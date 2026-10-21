from __future__ import annotations

import logging
import random
import time

from abcvaultbot.client import VaultClient
from abcvaultbot.config import AppConfig
from abcvaultbot.notifications import Notifier
from abcvaultbot.parser import (
    is_login_redirect,
    is_vault_closed,
    parse_products,
    title_matches_keywords,
)

logger = logging.getLogger(__name__)


class Monitor:
    def __init__(
        self, config: AppConfig, client: VaultClient, notifier: Notifier
    ) -> None:
        self.config = config
        self.client = client
        self.notifier = notifier

    def run(self) -> None:
        logger.info("Validating Vault Key...")
        if not self.client.validate_vault_key():
            raise RuntimeError(
                "Invalid Vault Key — check the code from your invitation email."
            )

        logger.info("Signing in to The Vault...")
        self.client.login()

        while True:
            try:
                self._poll_once()
            except SystemExit:
                raise
            except Exception as exc:
                logger.exception("Poll error: %s", exc)

            sleep_for = self.config.monitor.poll_interval_seconds + random.uniform(
                0, self.config.monitor.poll_jitter_seconds
            )
            time.sleep(sleep_for)

    def _poll_once(self) -> None:
        html = self.client.fetch_page(self.config.monitor.shop_url)

        if is_vault_closed(html):
            logger.info("Vault appears closed; waiting for next poll...")
            return

        if is_login_redirect(html) and "data-product-id" not in html:
            logger.warning("Session may have expired; re-logging in...")
            self.client.login()
            html = self.client.fetch_page(self.config.monitor.shop_url)

        products = parse_products(html)
        if not products:
            logger.info("No products parsed from shop page yet.")
            return

        candidates = [
            p
            for p in products
            if title_matches_keywords(p.title, self.config.monitor.keywords)
        ]
        if not candidates:
            logger.debug("No keyword matches in %s products.", len(products))
            return

        inventory = self.client.check_inventory([p.sku for p in candidates])
        in_stock = [p for p in candidates if inventory.get(p.sku)]

        if not in_stock:
            logger.info(
                "Matched %s product(s) by keyword but none in stock.", len(candidates)
            )
            return

        target = in_stock[0]
        logger.info("In stock: %s (%s)", target.title, target.price or "price unknown")

        if not self.config.monitor.auto_add_to_cart:
            self.notifier.send(
                "Vault match (in stock)",
                f"{target.title}\n{target.url}",
            )
            if self.config.monitor.stop_after_cart:
                raise SystemExit(0)
            return

        result = self.client.add_to_cart(target.product_id, target.sku)
        message = (
            f"{target.title}\n"
            f"Price: {target.price or 'unknown'}\n"
            f"Cart: {result['cart_url']}\n"
            f"Complete checkout within ~4 minutes."
        )
        self.notifier.send("Added to Vault cart", message)

        if self.config.monitor.stop_after_cart:
            raise SystemExit(0)
