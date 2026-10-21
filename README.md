# ABC Vault Bot

Python monitor for [The ABC Vault](https://theabcvault.com) that watches for bottles matching your keywords, checks inventory, optionally adds to cart, and notifies you (including **Discord** on phone and desktop).

Inspired by [ABC BourBot](https://abcbourbot.com/), but self-hosted and configurable in YAML.

## Quick start (Windows)

**New to this?** Follow **[SETUP.md](SETUP.md)** — step-by-step with screenshots-level detail.

1. Install Python 3.10+ ([python.org](https://www.python.org/downloads/), check **Add to PATH**)
2. Double-click **`setup.bat`**
3. Edit **`config.yaml`** (ABC login, Vault key, keywords, Discord webhook)
4. On Vault day, double-click **`run.bat`**

## Important

- Invitation-only: you need a **Vault Key** from ABC’s email and an ABC online account.
- Automated access may violate ABC policy — personal use at your own risk.
- After add-to-cart, checkout within about **4 minutes**.

## Run from terminal (optional)

```bash
.venv\Scripts\activate
python -m abcvaultbot -c config.yaml
python -m abcvaultbot -c config.yaml -v   # verbose
```

## Notifications

- **console** — messages in the run window
- **desktop** — Windows toast (`pip install win10toast`, set `desktop: true`)
- **discord** — channel webhook; enable push notifications in the Discord app

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
