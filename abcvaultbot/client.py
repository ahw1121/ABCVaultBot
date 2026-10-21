from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any
from urllib.parse import unquote

import cloudscraper
import requests

from abcvaultbot.config import VaultConfig
from abcvaultbot.parser import extract_graphql_token

logger = logging.getLogger(__name__)

CUSTOMER_ATTRIBUTES_QUERY = """
query CustomerAttributes {
  customer {
    entityId
    email
    firstName
    lastName
  }
}
""".strip()


@dataclass
class CustomerInfo:
    entity_id: int
    email: str


class VaultClient:
    """HTTP client for The ABC Vault (BigCommerce + ABC middleware APIs)."""

    def __init__(self, config: VaultConfig) -> None:
        self.config = config
        self.session = cloudscraper.create_scraper(
            browser={"browser": "chrome", "platform": "windows", "mobile": False}
        )
        self._graphql_token: str | None = None
        self._customer: CustomerInfo | None = None

    def _vault_headers(self) -> dict[str, str]:
        return {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Vault-Key": self.config.vault_key,
        }

    def _xsrf_header(self) -> dict[str, str]:
        token = self.session.cookies.get("XSRF-TOKEN")
        if not token:
            return {}
        return {"X-XSRF-TOKEN": unquote(token)}

    def _json_headers(self) -> dict[str, str]:
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            **self._xsrf_header(),
            **self._vault_headers(),
        }
        return headers

    def validate_vault_key(self) -> bool:
        url = f"{self.config.middleware_api}/api/vault/vault-key/check"
        response = self.session.get(url, headers=self._vault_headers(), timeout=30)
        if response.status_code == 401:
            return False
        if response.status_code != 200:
            logger.warning("vault key check HTTP %s", response.status_code)
            return False
        payload = response.json()
        return payload.get("status") == "ok"

    def login(self) -> None:
        login_page = f"{self.config.base_url}/login.php"
        self.session.get(login_page, timeout=30)

        response = self.session.post(
            f"{login_page}?action=check_login",
            data={
                "login_email": self.config.email,
                "login_pass": self.config.password,
            },
            timeout=30,
            allow_redirects=True,
        )
        if "login_email" in response.text and "Sign in" in response.text:
            raise RuntimeError(
                "Login failed — check email/password or whether today's Vault session allows sign-in."
            )

    def fetch_page(self, url: str) -> str:
        response = self.session.get(url, timeout=30)
        response.raise_for_status()
        return response.text

    def ensure_graphql_token(self, page_html: str | None = None) -> str:
        if self._graphql_token:
            return self._graphql_token
        html = page_html or self.fetch_page(self.config.base_url + "/shop/")
        token = extract_graphql_token(html)
        if not token:
            raise RuntimeError("Could not find graphQL token on shop page.")
        self._graphql_token = token
        return token

    def get_customer(self) -> CustomerInfo:
        if self._customer:
            return self._customer
        token = self.ensure_graphql_token()
        response = self.session.post(
            f"{self.config.base_url}/graphql",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}",
            },
            json={"query": CUSTOMER_ATTRIBUTES_QUERY},
            timeout=30,
        )
        response.raise_for_status()
        payload = response.json()
        customer = (payload.get("data") or {}).get("customer")
        if not customer or not customer.get("entityId"):
            raise RuntimeError(
                "Could not load customer profile — are you logged in with Vault access?"
            )
        self._customer = CustomerInfo(
            entity_id=int(customer["entityId"]),
            email=str(customer.get("email") or self.config.email),
        )
        return self._customer

    def check_inventory(self, skus: list[str]) -> dict[str, bool]:
        if not skus:
            return {}
        sku_param = ",".join(skus)
        url = (
            f"{self.config.middleware_api}/api/vault/inventory-check"
            f"?sku:in={sku_param}"
        )
        response = self.session.get(url, headers=self._vault_headers(), timeout=30)
        if response.status_code == 401:
            raise RuntimeError("Inventory check unauthorized — is the Vault Key valid?")
        response.raise_for_status()
        rows: list[dict[str, Any]] = response.json()
        result: dict[str, bool] = {}
        for row in rows:
            sku = str(row.get("sku", ""))
            result[sku] = bool(row.get("has_inventory"))
        return result

    def get_cart(self) -> list[dict[str, Any]]:
        response = self.session.get(
            f"{self.config.base_url}/api/storefront/carts",
            headers=self._json_headers(),
            timeout=30,
        )
        if response.status_code == 404:
            return []
        response.raise_for_status()
        data = response.json()
        return data if isinstance(data, list) else []

    def add_to_cart(self, product_id: int, sku: str) -> dict[str, Any]:
        customer = self.get_customer()
        carts = self.get_cart()
        if carts:
            cart_id = carts[0]["id"]
            self._add_line_item(cart_id, product_id)
        else:
            cart = self._create_cart(product_id)
            cart_id = cart["id"]

        reserve_url = f"{self.config.middleware_api}/api/vault/cart-reserve"
        reserve_body = {
            "cart_id": cart_id,
            "customer_id": customer.entity_id,
            "customer_email": customer.email,
            "product_id": product_id,
            "sku": sku,
            "quantity": 1,
        }
        reserve_response = self.session.post(
            reserve_url,
            headers=self._json_headers(),
            json=reserve_body,
            timeout=30,
        )
        reserve_response.raise_for_status()
        return {
            "cart_id": cart_id,
            "cart_url": f"{self.config.base_url}/cart.php",
            "reserve": reserve_response.json(),
        }

    def _create_cart(self, product_id: int) -> dict[str, Any]:
        body = {"lineItems": [{"productId": product_id, "quantity": 1}]}
        response = self.session.post(
            f"{self.config.base_url}/api/storefront/carts",
            headers=self._json_headers(),
            json=body,
            timeout=30,
        )
        response.raise_for_status()
        return response.json()

    def _add_line_item(self, cart_id: str, product_id: int) -> None:
        body = {"lineItems": [{"productId": product_id, "quantity": 1}]}
        response = self.session.post(
            f"{self.config.base_url}/api/storefront/carts/{cart_id}/items",
            headers=self._json_headers(),
            json=body,
            timeout=30,
        )
        if response.status_code >= 400:
            logger.warning(
                "add line item returned %s: %s",
                response.status_code,
                response.text[:300],
            )
