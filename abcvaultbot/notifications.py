from __future__ import annotations

import logging
from dataclasses import dataclass

import requests

from abcvaultbot.config import NotificationConfig

logger = logging.getLogger(__name__)

DISCORD_CONTENT_LIMIT = 2000


@dataclass
class Notifier:
    config: NotificationConfig

    def send(self, title: str, message: str) -> None:
        if self.config.console:
            print(f"\n=== {title} ===\n{message}\n")
        if self.config.desktop:
            self._desktop(title, message)
        if self.config.discord.enabled:
            self._discord(title, message)

    def _desktop(self, title: str, message: str) -> None:
        try:
            from win10toast import ToastNotifier  # type: ignore[import-untyped]

            ToastNotifier().show_toast(title, message, duration=10, threaded=True)
        except ImportError:
            logger.warning("desktop notifications need: pip install win10toast")
        except Exception as exc:
            logger.warning("desktop notification failed: %s", exc)

    def _discord(self, title: str, message: str) -> None:
        url = self.config.discord.webhook_url.strip()
        if not url:
            logger.warning("discord enabled but webhook_url is missing")
            return
        body_text = f"**{title}**\n\n{message}"
        if len(body_text) > DISCORD_CONTENT_LIMIT:
            body_text = body_text[: DISCORD_CONTENT_LIMIT - 3] + "..."
        payload = {
            "content": body_text,
            "allowed_mentions": {"parse": []},
        }
        try:
            response = requests.post(url, json=payload, timeout=15)
            if response.status_code >= 400:
                logger.warning(
                    "discord notification failed: HTTP %s %s",
                    response.status_code,
                    response.text[:200],
                )
        except requests.RequestException as exc:
            logger.warning("discord notification failed: %s", exc)
