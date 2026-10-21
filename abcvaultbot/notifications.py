from __future__ import annotations

import logging
from dataclasses import dataclass

import requests

from abcvaultbot.config import NotificationConfig

logger = logging.getLogger(__name__)


@dataclass
class Notifier:
    config: NotificationConfig

    def send(self, title: str, message: str) -> None:
        if self.config.console:
            print(f"\n=== {title} ===\n{message}\n")
        if self.config.desktop:
            self._desktop(title, message)
        if self.config.telegram.enabled:
            self._telegram(f"{title}\n{message}")
        if self.config.webhook.enabled:
            self._webhook(title, message)

    def _desktop(self, title: str, message: str) -> None:
        try:
            from win10toast import ToastNotifier  # type: ignore[import-untyped]

            ToastNotifier().show_toast(title, message, duration=10, threaded=True)
        except ImportError:
            logger.warning("desktop notifications need: pip install win10toast")
        except Exception as exc:
            logger.warning("desktop notification failed: %s", exc)

    def _telegram(self, text: str) -> None:
        token = self.config.telegram.bot_token
        chat_id = self.config.telegram.chat_id
        if not token or not chat_id:
            logger.warning("telegram enabled but bot_token or chat_id is missing")
            return
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        try:
            requests.post(
                url,
                json={"chat_id": chat_id, "text": text},
                timeout=15,
            )
        except requests.RequestException as exc:
            logger.warning("telegram notification failed: %s", exc)

    def _webhook(self, title: str, message: str) -> None:
        url = self.config.webhook.url
        if not url:
            logger.warning("webhook enabled but url is missing")
            return
        try:
            requests.post(
                url,
                json={"title": title, "message": message},
                timeout=15,
            )
        except requests.RequestException as exc:
            logger.warning("webhook notification failed: %s", exc)
