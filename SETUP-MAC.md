# ABC Vault Bot — Mac setup guide

This guide is for **macOS** and assumes little terminal experience. You need a **Vault invitation** from ABC (email with a **Vault Key**) and an **ABC online account** (same login as [abcfws.com](https://abcfws.com)).

Windows users: see **[SETUP.md](SETUP.md)**.

---

## Step 1: Install Python (one time)

**Option A — python.org (simplest)**

1. Open [https://www.python.org/downloads/macos/](https://www.python.org/downloads/macos/)
2. Download the latest **Python 3** installer for Mac
3. Run the installer and complete the steps

**Option B — Homebrew** (if you already use Homebrew)

```bash
brew install python3
```

Check that Python works: open **Terminal** (Spotlight → type `Terminal`) and run:

```bash
python3 --version
```

You should see something like `Python 3.12.x`.

---

## Step 2: Get the bot folder

1. Unzip **ABCVaultBot** to a simple location, e.g. `Documents/ABCVaultBot`
2. In Terminal, go to that folder (adjust the path if yours is different):

```bash
cd ~/Documents/ABCVaultBot
```

---

## Step 3: Run setup (one time)

The first time only, allow the scripts to run and install dependencies:

```bash
chmod +x setup.sh run.sh
./setup.sh
```

If macOS says the file is “from an unidentified developer,” you can still run it from Terminal as above. For double-clicking in Finder later, right-click the script → **Open** once to approve.

When setup finishes, you should have a `config.yaml` file (copied from the example).

---

## Step 4: Edit your settings (`config.yaml`)

1. Open **`config.yaml`** in **TextEdit** (or any text editor)
   - In Finder: right-click `config.yaml` → **Open With** → **TextEdit**
   - Make sure TextEdit is in **plain text** mode (Format → Make Plain Text) so quotes stay correct
2. Fill in:

| Setting | What to enter |
|--------|----------------|
| `vault.email` | Your ABC account email |
| `vault.password` | Your ABC password |
| `vault.vault_key` | The code from your Vault invitation email (paste when you get it) |
| `monitor.keywords` | Words that appear in bottle names you want (one per line with `-`) |

**Example keywords:** For Maker’s Mark, use `"Maker"` or `"Maker's Mark"` — copy part of the name from the Vault shop page.

**First-time test (recommended):** Set `auto_add_to_cart: false` so the bot only alerts you and does not add to cart. Set it back to `true` when you are ready.

3. Save the file (**File → Save**)

**Never send `config.yaml` to anyone** — it contains your password and Vault key.

---

## Step 5: Discord alerts on your phone (recommended)

Discord can push to your **iPhone** and **Mac** when a bottle matches.

### Create a webhook

1. Install **Discord** on your phone and Mac
2. Create a server (or use one you have)
3. Create a channel (e.g. `#vault-alerts`)
4. Click the **gear** next to the channel → **Integrations** → **Webhooks** → **New Webhook**
5. Name it (e.g. `Vault Bot`), click **Copy Webhook URL**

### Paste into config

In `config.yaml`:

```yaml
notifications:
  discord:
    enabled: true
    webhook_url: "paste-the-full-url-here"
```

Save the file. Keep the webhook URL private.

---

## Step 6: Run on Vault day

1. Paste today’s **Vault key** into `config.yaml` if it changed
2. Prevent sleep while monitoring:
   - **System Settings → Displays → Advanced** (or **Battery → Options**) and disable sleep on power adapter, or
   - Leave the Mac plugged in and use **System Settings → Lock Screen** to set “Turn display off” to **Never** while the bot runs
3. In Terminal:

```bash
cd ~/Documents/ABCVaultBot
./run.sh
```

4. Leave Terminal open; you should see log lines every few seconds
5. Stop with **Ctrl+C**

When a bottle is added to your cart, you have about **4 minutes** to checkout on [theabcvault.com](https://theabcvault.com) (Safari on Mac or Discord alert on phone).

### Optional: run from Finder

After `chmod +x run.sh`, you can drag **Terminal** to the Dock, `cd` to the folder once, then run `./run.sh`. Some users create a **Shortcut** or small script in Automator that opens Terminal and runs `./run.sh` — optional.

---

## Optional: Mac notification banner

In `config.yaml`, set:

```yaml
notifications:
  desktop: true
```

The bot uses macOS **Notification Center** (no extra install). Discord is still best for phone alerts.

---

## Troubleshooting

| Problem | What to try |
|--------|-------------|
| `command not found: python3` | Install Python (Step 1) or use the python.org installer |
| `Permission denied` on `./setup.sh` | Run `chmod +x setup.sh run.sh` |
| `Invalid Vault Key` | Copy the key again from today’s email |
| `Login failed` | Check email/password; you may have already purchased today |
| No Discord message | `enabled: true`, webhook URL in quotes, notifications on in Discord app |
| Mac went to sleep | Plug in power and adjust sleep settings (Step 6) |

---

## Run from terminal (manual)

```bash
cd ~/Documents/ABCVaultBot
source .venv/bin/activate
python -m abcvaultbot -c config.yaml
python -m abcvaultbot -c config.yaml -v   # verbose
```

---

## Sharing with a friend

Send the project **without** your `config.yaml`. On Mac they follow this guide: `./setup.sh`, edit their own config, `./run.sh` on drop day.

---

## Legal note

ABC’s site rules discourage automated tools. Use at your own risk, for personal use only.
