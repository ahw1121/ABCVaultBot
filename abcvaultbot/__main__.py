from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

from abcvaultbot.client import VaultClient
from abcvaultbot.config import load_config, validate_config
from abcvaultbot.monitor import Monitor
from abcvaultbot.notifications import Notifier


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Monitor Florida ABC Vault for bourbon keywords and add matches to cart."
    )
    parser.add_argument(
        "-c",
        "--config",
        type=Path,
        default=Path("config.yaml"),
        help="Path to YAML config (default: config.yaml)",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable debug logging",
    )
    args = parser.parse_args(argv)

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )

    if not args.config.exists():
        print(
            f"Config not found: {args.config}\n"
            "Copy config.example.yaml to config.yaml and add your credentials.",
            file=sys.stderr,
        )
        return 1

    config = load_config(args.config)
    validate_config(config)

    client = VaultClient(config.vault)
    notifier = Notifier(config.notifications)
    monitor = Monitor(config, client, notifier)

    try:
        monitor.run()
    except KeyboardInterrupt:
        print("\nStopped.")
        return 0
    except SystemExit:
        return 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
