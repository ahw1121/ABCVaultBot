# ABC Vault Bot

Python monitor for [The ABC Vault](https://theabcvault.com) that watches for bottles matching your keywords, checks inventory, optionally adds to cart, and notifies you (including **Discord** on phone and desktop).

Inspired by [ABC BourBot](https://abcbourbot.com/), but self-hosted and configurable in YAML.

## Quick start

| Platform | Setup guide | Run |
|----------|-------------|-----|
| **Windows** | [SETUP.md](SETUP.md) | Double-click **`setup.bat`**, then **`run.bat`** |
| **Mac** | [SETUP-MAC.md](SETUP-MAC.md) | `./setup.sh`, then `./run.sh` |

1. Install Python 3.10+
2. Run setup once, edit **`config.yaml`** (ABC login, Vault key, keywords, Discord webhook)
3. On Vault day, run the bot and keep the computer awake

## Important

- Invitation-only: you need a **Vault Key** from ABC’s email and an ABC online account.
- Automated access may violate ABC policy — personal use at your own risk.
- After add-to-cart, checkout within about **4 minutes**.

## Run from terminal (optional)

**Windows**

```bash
.venv\Scripts\activate
python -m abcvaultbot -c config.yaml
```

**Mac / Linux**

```bash
source .venv/bin/activate
python -m abcvaultbot -c config.yaml
```

Add `-v` for verbose logging.

## Notifications

- **console** — messages in the terminal window
- **desktop** — Windows toast (`pip install win10toast`) or macOS Notification Center (`desktop: true`)
- **discord** — channel webhook; enable push in the Discord app

## How it works

1. Validate Vault key (ABC middleware API)
2. Log in to The Vault
3. Poll `/shop/`, match keywords in product titles
4. Check inventory for matches
5. Add to cart via BigCommerce + ABC cart-reserve APIs

## Tests

```bash
python -m unittest discover -s tests
```
