# Simple-Patreon-Discord-Announcer

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

## 🤖 Optional: Customizing Your Bot's Appearance

🤖 Optional: Customizing Bot Names

The bot's name is managed by Discord's webhook function, and is passed as part of the payload in the `patreon-announcer.py` file.

To set a unique name for your bot's appearance in Discord, simply edit the `DISCORD_BOTNAME` at the beginning of the `patreon-announcer.py` file to your desired name.

Further reading: https://birdie0.github.io/discord-webhooks-guide/structure/username.html

🤖 Optional: Customizing Bot Avatars

The bot's avatar is also managed by Discord's webhooks, and is passed similarly. Simply set the `DISCORD_BOT_AVATAR` variable in the `patreon-announcer.py` file to an image link, and the webhook should use your image. Avatars should follow the usual Discord avatar guidelines related to resolution and composition.

Example: https://birdie0.github.io/discord-webhooks-guide/structure/avatar_url.html

## ⚙️ Optional: Customizing Messages

⚙️ Optional: Customizing Messages by Tier

To customize Discord messages with tier-specific text or emojis, update the TIER_EMOJI_MAP section in patreon-announcer.py:

```
TIER_EMOJI_MAP = {
    "12345678": "🔥**Exclusive!**🔥|",  # Example: top-tier patrons only
    "87654321": "🧪**Public!**🧪|",  # Example: free-tier availability
    # Add more as needed
}
DEFAULT_EMOJI = "📢New Post!"
```

🔍 How to Find Your Tier IDs

To look up your Patreon tier IDs:

    Run setup/tier_identifier.py locally.

    The script will print out a list of tier IDs, names, descriptions, and pricing.

    Copy the IDs you want into the TIER_EMOJI_MAP to customize messages.

    The script uses your PATREON_ACCESS_TOKEN—make sure it's set as an environment variable or hardcoded while testing.

---

## 🛠 Files and Behavior

- `patreon-announcer.py`: Main script
- `setup/tier_identify.py`: Optional setup script; identifies and prints your unique tier levels, to enable unique discord messages per tier.
- `.github/workflows/patreon-bot.yml`: Defines schedule (default: every 30 mins)
- `recent_posts.json`: Stores recent post IDs to avoid duplicates. Generated as part of your Github Actions workflow and cached between runs.

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
A: Yes—just export your secrets as environment variables and run `patreon-announcer.py`.

**Q: How do I enable unique message formats for each tier?**  
A: You'll need to identify your patron tier ID's; each tier has a unique ID in Patreon's backend. These can be identified by running `setup/tier_identifier.py` locally.

