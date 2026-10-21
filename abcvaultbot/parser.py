from __future__ import annotations

import html
import re
from dataclasses import dataclass

from bs4 import BeautifulSoup

GRAPHQL_TOKEN_RE = re.compile(
    r'graphQLToken\\":\\"([^"\\]+)|graphQlKey\s*=\s*"([^"]+)"'
)


@dataclass(frozen=True)
class Product:
    product_id: int
    sku: str
    title: str
    url: str
    price: str | None = None


def extract_graphql_token(page_html: str) -> str | None:
    match = GRAPHQL_TOKEN_RE.search(page_html)
    if not match:
        return None
    return match.group(1) or match.group(2)


def parse_products(shop_html: str) -> list[Product]:
    soup = BeautifulSoup(shop_html, "html.parser")
    products: list[Product] = []
    for article in soup.select("article.card[data-product-id]"):
        product_id_raw = article.get("data-product-id")
        sku = article.get("data-product-sku")
        if not product_id_raw or not sku:
            continue
        title_el = article.select_one("h3.card-title a")
        if not title_el:
            continue
        title = html.unescape(title_el.get_text(strip=True))
        url = title_el.get("href", "")
        price_el = article.select_one("[data-product-price-without-tax]")
        price = price_el.get_text(strip=True) if price_el else None
        products.append(
            Product(
                product_id=int(product_id_raw),
                sku=str(sku),
                title=title,
                url=url,
                price=price,
            )
        )
    return products


def title_matches_keywords(title: str, keywords: list[str]) -> bool:
    if not keywords:
        return False
    normalized = title.casefold()
    return any(keyword.casefold() in normalized for keyword in keywords if keyword)


def is_vault_closed(page_html: str) -> bool:
    lowered = page_html.casefold()
    return "the vault is now closed" in lowered and "shop the vault" not in lowered


def is_login_redirect(page_html: str) -> bool:
    return 'window.location.href="/login.php"' in page_html
