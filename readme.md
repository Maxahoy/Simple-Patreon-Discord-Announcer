# 🧪 FemmeBot Patreon-to-Discord Poster

This GitHub Actions bot checks a creator's Patreon page for new posts and notifies a Discord channel via webhook—automatically and securely.

- 🔗 Posts are linked directly (no content reposting).
- 🔐 No need to share your Patreon credentials with anyone else.
- 💬 Custom Discord messages based on Patreon tiers (optional).
- 🕐 Scheduled to check every 15–60 minutes, configurable per your preferences.

---

## 📸 Screenshots

> [Insert screenshot: Discord message example here]

> [Insert screenshot: GitHub Secrets config here]

---

## 🚀 Setup & Configuration

### 1. **Fork the Repository**

Click the "Fork" button on the top-right of this repository to make your own copy.

---

### 2. **Create a Discord Webhook**

- Go to your Discord server
- Open **Server Settings → Integrations → Webhooks**
- Create a new webhook and copy the URL

> [Insert screenshot: Discord webhook setup here]

---

### 3. **Create a Patreon OAuth Client**

1. Go to [Patreon Developer Portal](https://www.patreon.com/portal/registration/register-clients)
2. Register a new API client as a **"Creator"**
3. Get the following:
   - `Client ID`
   - `Client Secret`
   - Generate an **Access Token** with `campaigns` and `posts` scopes

> [Insert screenshot: Patreon OAuth registration form here]

---

### 4. **Set GitHub Secrets**

Go to your forked repo → **Settings → Secrets and Variables → Actions**

Add the following secrets:

| Name                  | Description                        |
|-----------------------|------------------------------------|
| `DISCORD_WEBHOOK_URL` | Your Discord webhook URL           |
| `PATREON_TOKEN`       | Creator access token (OAuth token) |

> [Insert screenshot: GitHub Secrets interface here]

---

### 5. **Enable GitHub Actions**

No need to manually activate anything—just commit or push to your repo, or wait for the next scheduled run. To run manually:

- Go to **Actions**
- Select the workflow and click **Run workflow**

---

## ⚙️ Optional: Customizing Messages

In `femmebot_scraper.py`, you can modify the `format_discord_message()` function to:

- Add custom emojis based on tier IDs
- Format titles or add creator branding

> Tier IDs are exposed via the Patreon API and can be added to a dictionary inside the script.

---

## 🛠 Files and Behavior

- `femmebot_scraper.py`: Main script
- `.github/workflows/patreon-bot.yml`: Defines schedule (default: every 30 mins)
- `recent_posts.json`: Stores last 5 post IDs to avoid duplicates

---

## ❓ FAQ

**Q: The bot isn’t posting anything.**  
A: Make sure:
- Your token has proper scopes
- There’s at least one public or patron-only post
- You ran the GitHub Action manually or waited for the schedule

**Q: Can I post to different channels based on tier?**  
A: Not yet, but tier-based message formatting is already supported and can be extended.

**Q: Can I run this locally instead of GitHub Actions?**  
A: Yes—just export your secrets as environment variables and run `femmebot_scraper.py`.

---

## 🧾 License

MIT License. Feel free to fork, modify, and contribute!

---

## 👩‍🔬 Credits

Created with love for [Your Creator Name Here].

