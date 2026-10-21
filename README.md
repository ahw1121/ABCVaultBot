# ABC Vault Bot

Python monitor for [The ABC Vault](https://theabcvault.com) that refreshes the shop, watches for bottles whose titles match your keywords, checks live inventory, and optionally adds the first match to your cart—then notifies you.

Inspired by the commercial [ABC BourBot](https://abcbourbot.com/) flow (Vault key → login → keyword list → inventory → cart), but self-hosted and configurable in YAML.

## Important

- The Vault is invitation-only. You need a valid **Vault Key** from ABC's email and an ABC online account.
- ABC's FAQ warns that automated access can lead to cancelled orders or bans. Use at your own risk; this tool is for personal use only.
- After add-to-cart, you have about **4 minutes** to finish checkout.

## Setup

```bash
cd ABCVaultBot
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy config.example.yaml config.yaml
```

Edit `config.yaml`:

- `vault.email` / `vault.password` — same as abcfws.com / The Vault
- `vault.vault_key` — code from your Vault invitation email
- `monitor.keywords` — substrings to match in product titles (case-insensitive, any match)
- `monitor.poll_interval_seconds` — how often to refresh (adds random jitter)

Optional notifications: console (default), Windows desktop (`pip install win10toast`), Telegram, or webhook.

## Run

```bash
python -m abcvaultbot -c config.yaml
```

Verbose logging:

```bash
python -m abcvaultbot -c config.yaml -v
```

## How it works

1. **Vault Key** — `GET https://abc.irishtitan.cloud/api/vault/vault-key/check` with `Vault-Key` header (same middleware the site theme uses).
2. **Login** — POST to `login.php?action=check_login` with your ABC credentials.
3. **Shop poll** — Fetches `/shop/`, parses product cards (`data-product-id`, `data-product-sku`, title).
4. **Inventory** — `GET .../api/vault/inventory-check?sku:in=...` for keyword matches only.
5. **Cart** — BigCommerce Storefront API `POST /api/storefront/carts` plus ABC `POST .../api/vault/cart-reserve` (mirrors the site's Buy Now flow).

## Future: Gmail Vault Key

A planned enhancement is OAuth/Gmail parsing to read the invitation email and extract the Vault Key automatically. For now, paste the key into `config.yaml` when you receive an invite.

## Tests

```bash
python -m unittest discover -s tests
```

Uses `tmp_shop.html` if present (downloaded during development); parser tests skip otherwise.
