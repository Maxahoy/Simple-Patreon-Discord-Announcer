import os
import json
import requests
from datetime import datetime

# Load secrets from environment
# CONFIGURATION: THESE NEED SETUP AS ENVIRONMENT VARIABLES IN GITHUB ACTIONS.
ACCESS_TOKEN = os.getenv("PATREON_ACCESS_TOKEN")
WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

HEADERS = {
    "Authorization": f"Bearer {ACCESS_TOKEN}"
}

CACHE_FILE = "recent_posts.json"
MAX_TRACKED_POSTS = 5

# CONFIGURATION: USING TIER-SPECIFIC EMOJI'S WILL REQUIRE KNOWLEDGE OF YOUR TIER ID'S.
# These can be identified using the script located in "testing/tier_identification.py", in a local environment.
# Adding additional tiers is supported -- the code should handle additional tier emoji mappings gracefully.
# Optional: Custom emojis or text for specific tier IDs
TIER_EMOJI_MAP = {
    "12345678": "🔥🔥",  # Example: top-tier patrons only
    "87654321": "🧪🧪",  # Example: free-tier availability
    # Add more as needed
}
DEFAULT_EMOJI = "📢"

def get_campaign_id():
    url = "https://www.patreon.com/api/oauth2/v2/campaigns"
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch campaign ID: {response.status_code} {response.text}")

    data = response.json()
    campaigns = data.get("data", [])
    if not campaigns:
        raise Exception("No campaigns found for the access token provided.")
    print("Campaign id: ", campaigns[0]["id"])
    return campaigns[0]["id"]  # Only use the first campaign found

def fetch_latest_posts(campaign_id, limit=5):
    url = f"https://www.patreon.com/api/oauth2/v2/campaigns/{campaign_id}/posts"
    params = {
        "sort": "-published_at",
        "page[count]": limit,
        "fields[post]": "title,url,published_at"
    }
    response = requests.get(url, headers=HEADERS, params=params)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch posts: {response.status_code} {response.text}")

    data = response.json()
    posts = data.get("data", [])
    print(posts)
    return [
        {
            "id": post["id"],
            "title": post.get("attributes", {}).get("title", "(Untitled)"),
            "url": post.get("attributes", {}).get("url", "URL not found"),
            "published_at": post.get("attributes", {}).get("published_at", "")
        }
        for post in posts
    ]


def load_cached_post_ids():
    if not os.path.exists(CACHE_FILE):
        return []
    with open(CACHE_FILE, "r") as f:
        return json.load(f)

def save_cached_post_ids(post_ids):
    with open(CACHE_FILE, "w") as f:
        json.dump(post_ids[:MAX_TRACKED_POSTS], f)
        
def format_discord_message(post):
    title = post.get("title", "(Untitled)")
    url = "https://www.patreon.com/" + post.get("url", "#")

    # Grab the first tier ID (or none)
    tier_ids = post.get("tier_ids", [])
    matched_emoji = DEFAULT_EMOJI

    for tier_id in tier_ids:
        if tier_id in TIER_EMOJI_MAP:
            matched_emoji = TIER_EMOJI_MAP[tier_id]
            break

    return f"{matched_emoji} New Patreon Post: [{title}]({url})"


def send_to_discord(post):

    content = format_discord_message(post)
    payload = {
        "username": "Femmebot",
        "content": content
        # No avatar_url provided — will use Discord's default
    }

    response = requests.post(WEBHOOK_URL, json=payload)
    if response.status_code != 204:
        raise Exception(f"Failed to send webhook: {response.status_code} {response.text}")

def main():
    try:
        print("Attempting to fetch campaign ID")
        campaign_id = get_campaign_id()  # No argument needed here
        print("Campaign ID fetched.")
        posts = fetch_latest_posts(campaign_id)

        cached_ids = load_cached_post_ids()
        new_posts = [p for p in posts if p["id"] not in cached_ids]

        if not new_posts:
            print("No new posts.")
            return

        # Newest first, send in reverse so oldest is posted first
        for post in reversed(new_posts):
            send_to_discord(post)
            print(f"Posted: {post['title']} ({post['url']})")

        # Update the cache
        all_ids = [p["id"] for p in new_posts] + cached_ids
        save_cached_post_ids(all_ids)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
