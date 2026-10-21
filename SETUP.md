# ABC Vault Bot — Easy setup guide

This guide assumes **Windows** and little command-line experience. You need a **Vault invitation** from ABC (email with a **Vault Key**) and an **ABC online account** (same login as [abcfws.com](https://abcfws.com)).

---

## Step 1: Install Python (one time)

1. Open [https://www.python.org/downloads/](https://www.python.org/downloads/)
2. Click **Download Python 3.x**
3. Run the installer
4. **Important:** On the first screen, check **“Add python.exe to PATH”**
5. Click **Install Now**

---

## Step 2: Set up the bot (one time)

1. Unzip the **ABCVaultBot** folder somewhere easy to find (e.g. `Documents\ABCVaultBot`)
2. Double-click **`setup.bat`**
3. Wait until it says **Setup complete**
4. If it says Python was not found, go back to Step 1

---

## Step 3: Edit your settings (`config.yaml`)

1. In the ABCVaultBot folder, open **`config.yaml`** with **Notepad** (right-click → Open with → Notepad)
2. Fill in:

| Setting | What to enter |
|--------|----------------|
| `vault.email` | Your ABC account email |
| `vault.password` | Your ABC password |
| `vault.vault_key` | The code from your Vault invitation email (paste when you get it) |
| `monitor.keywords` | Words that appear in bottle names you want (one per line with `-`) |

**Example keywords:** If you want Maker’s Mark, use `"Maker"` or `"Maker's Mark"` — copy part of the name from the Vault shop page.

**First-time test (recommended):** Set `auto_add_to_cart: false` so the bot only alerts you and does not add anything to the cart. Set it back to `true` when you are ready for real drops.

3. Save the file (File → Save)

**Never send `config.yaml` to anyone** — it contains your password and Vault key.

---

## Step 4: Discord alerts on your phone (recommended)

Discord can push to your **phone** and **computer** when a bottle matches.

### Create a webhook

1. Install **Discord** on your phone and PC (or use the browser)
2. Create a server for yourself (or use one you already have)
3. Create a channel (e.g. `#vault-alerts`)
4. Click the **gear** next to the channel name → **Integrations** → **Webhooks** → **New Webhook**
5. Name it (e.g. `Vault Bot`), pick the channel, click **Copy Webhook URL**

### Paste into config

In `config.yaml`, under `notifications.discord`:

```yaml
discord:
  enabled: true
  webhook_url: "paste-the-full-url-here"
```

Save the file. Only you should have this URL — anyone with it can post to your channel.

### Test (optional)

After setup, when the bot finds a match you should see a message in that Discord channel and get a phone notification if Discord notifications are on.

---

## Step 5: Run on Vault day

1. Paste today’s **Vault key** into `config.yaml` if it changed
2. Plug in the PC and turn off sleep (Settings → System → Power → **Never** while monitoring)
3. Double-click **`run.bat`**
4. Leave the window open. You should see log lines every few seconds
5. To stop: click the window and press **Ctrl+C**, or close the window

When a bottle is added to your cart, you have about **4 minutes** to finish checkout on [theabcvault.com](https://theabcvault.com) (phone or computer browser).

---

## Optional: Windows popup on this PC

In `config.yaml`, set `notifications.desktop: true`, then in a terminal (after `setup.bat`):

```text
pip install win10toast
```

(Or run `setup.bat` again after adding win10toast to requirements if we add it — for now user runs pip manually; I could add win10toast to requirements as optional - README says pip install. I'll add to SETUP only)

---

## Troubleshooting

| Problem | What to try |
|--------|-------------|
| “Python was not found” | Reinstall Python with **Add to PATH** checked, then run `setup.bat` again |
| “Invalid Vault Key” | Copy the key again from today’s email; invites are time-limited |
| “Login failed” | Check email/password; you may already have purchased today |
| No Discord message | Check `enabled: true`, webhook URL in quotes, Discord notifications on |
| Window closes instantly | Run `setup.bat` first; read any error before the window closes |

---

## Sharing with a friend

Send them the project folder **without** your `config.yaml`. They run **`setup.bat`**, create their own **`config.yaml`**, and use their own ABC account and Vault key.

---

## Legal note

ABC’s site rules discourage automated tools. Use at your own risk, for personal use only.
