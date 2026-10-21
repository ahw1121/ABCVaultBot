from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


@dataclass
class VaultConfig:
    base_url: str = "https://theabcvault.com"
    middleware_api: str = "https://abc.irishtitan.cloud"
    email: str = ""
    password: str = ""
    vault_key: str = ""
    store_id: str | None = None


@dataclass
class MonitorConfig:
    shop_url: str = "https://theabcvault.com/shop/"
    poll_interval_seconds: float = 3.0
    poll_jitter_seconds: float = 1.5
    keywords: list[str] = field(default_factory=list)
    auto_add_to_cart: bool = True
    stop_after_cart: bool = True


@dataclass
class DiscordConfig:
    enabled: bool = False
    webhook_url: str = ""


@dataclass
class NotificationConfig:
    console: bool = True
    desktop: bool = False
    discord: DiscordConfig = field(default_factory=DiscordConfig)


@dataclass
class AppConfig:
    vault: VaultConfig = field(default_factory=VaultConfig)
    monitor: MonitorConfig = field(default_factory=MonitorConfig)
    notifications: NotificationConfig = field(default_factory=NotificationConfig)


def _section(data: dict[str, Any], key: str) -> dict[str, Any]:
    value = data.get(key)
    return value if isinstance(value, dict) else {}


def load_config(path: Path | str) -> AppConfig:
    path = Path(path)
    raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}

    vault_raw = _section(raw, "vault")
    monitor_raw = _section(raw, "monitor")
    notif_raw = _section(raw, "notifications")
    discord_raw = _section(notif_raw, "discord")

    keywords = monitor_raw.get("keywords") or []
    if not isinstance(keywords, list):
        raise ValueError("monitor.keywords must be a list of strings")

    return AppConfig(
        vault=VaultConfig(
            base_url=str(vault_raw.get("base_url", VaultConfig.base_url)),
            middleware_api=str(
                vault_raw.get("middleware_api", VaultConfig.middleware_api)
            ),
            email=str(vault_raw.get("email", "")),
            password=str(vault_raw.get("password", "")),
            vault_key=str(vault_raw.get("vault_key", "")),
            store_id=vault_raw.get("store_id"),
        ),
        monitor=MonitorConfig(
            shop_url=str(monitor_raw.get("shop_url", MonitorConfig.shop_url)),
            poll_interval_seconds=float(
                monitor_raw.get(
                    "poll_interval_seconds", MonitorConfig.poll_interval_seconds
                )
            ),
            poll_jitter_seconds=float(
                monitor_raw.get(
                    "poll_jitter_seconds", MonitorConfig.poll_jitter_seconds
                )
            ),
            keywords=[str(k) for k in keywords],
            auto_add_to_cart=bool(
                monitor_raw.get("auto_add_to_cart", MonitorConfig.auto_add_to_cart)
            ),
            stop_after_cart=bool(
                monitor_raw.get("stop_after_cart", MonitorConfig.stop_after_cart)
            ),
        ),
        notifications=NotificationConfig(
            console=bool(notif_raw.get("console", True)),
            desktop=bool(notif_raw.get("desktop", False)),
            discord=DiscordConfig(
                enabled=bool(discord_raw.get("enabled", False)),
                webhook_url=str(discord_raw.get("webhook_url", "")),
            ),
        ),
    )


def validate_config(config: AppConfig) -> None:
    missing: list[str] = []
    if not config.vault.email:
        missing.append("vault.email")
    if not config.vault.password:
        missing.append("vault.password")
    if not config.vault.vault_key:
        missing.append("vault.vault_key")
    if not config.monitor.keywords:
        missing.append("monitor.keywords (at least one)")
    if missing:
        raise ValueError("Missing required config: " + ", ".join(missing))
