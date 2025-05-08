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
MAX_TRACKED_POSTS = 10

DISCORD_BOTNAME = "Patreon Announcer"
# add a link to an avatar if you want; otherwise, leaving this field blank will use the standard discord default avatar.
#Example: https://birdie0.github.io/discord-webhooks-guide/structure/avatar_url.html
DISCORD_BOT_AVATAR = ""

# CONFIGURATION: USING TIER-SPECIFIC EMOJI'S WILL REQUIRE KNOWLEDGE OF YOUR TIER ID'S.
# These can be identified using the script located in "setup/tier_identification.py", in a local environment.
# Adding additional tiers is supported -- the code should handle additional tier emoji mappings gracefully.
# Optional: Custom emojis or text for specific tier IDs
TIER_EMOJI_MAP = {
    "25836975": "🔥**Exclusive!**🔥|",  # Example: top-tier patrons only
    "25832397": "🧪**Public Announcement!**🧪|",  # Example: free-tier availability
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

def fetch_latest_posts(campaign_id, limit=MAX_TRACKED_POSTS):
    url = f"https://www.patreon.com/api/oauth2/v2/campaigns/{campaign_id}/posts"
    params = {
        "page[size]": 100,  # Fetch up to 100 posts per request
        "fields[post]": "title,url,tiers,published_at"
    }
    
    all_posts = []
    cursor = None

    while True:
        if cursor:
            params["page[cursor]"] = cursor

        response = requests.get(url, headers=HEADERS, params=params)
        
        if response.status_code != 200:
            raise Exception(f"Failed to fetch posts: {response.status_code} {response.text}")

        data = response.json()
        posts = data.get("data", [])
        all_posts.extend(posts)

        next_cursor_url = data.get("links", {}).get("next")
        if next_cursor_url:
            cursor_param = next_cursor_url.split("page%5Bcursor%5D=")[-1].split("&")[0]
            cursor = cursor_param
        else:
            break  # No more pages

    # Sort posts by the 'published_at' field in descending order (newest first)
    # NOTE: Patreon's API does not respect sorting in the "published" at order. Hence, we grab all posts and sort them manually.
    # If patreon's api respected this, then we would grab fewer posts at a time and make fewer paginated requests, but alas.
    # My test page has a limited number of posts anyways (under 100) so this is not really an issue here.
    # For pages with thousands of posts, this could be an issue, but unlikely.
    all_posts = sorted(all_posts, key=lambda x: x['attributes']['published_at'], reverse=True)
    #print("\n\n")
    #print(all_posts)
    #print("\n\n\n")
    # Return a formatted list of posts
    return [
        {
            "id": post["id"],
            "title": post.get("attributes", {}).get("title", "(Untitled)"),
            "tiers": post.get("attributes", {}).get("tiers", "No tiers"),
            "url": post.get("attributes", {}).get("url", "URL not found"),
            "published_at": post.get("attributes", {}).get("published_at", "")
        }
        for post in all_posts[:limit]
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
    print("Post tier identifier")

    # Grab the first tier ID (or none)
    tier_ids = post.get("tiers", [])
    
    # Print tier IDs to ensure correct format
    print(f"Tier IDs in the post: {tier_ids}")

    matched_emoji = DEFAULT_EMOJI

    for tier_id in tier_ids:
        # Ensure tier_id is a string
        tier_id = str(tier_id)
        print(f"Checking this tier id: {tier_id}")
        if tier_id in TIER_EMOJI_MAP:
            matched_emoji = TIER_EMOJI_MAP[tier_id]
            print(f"Matched emoji: {matched_emoji}")
            break

    return f"{matched_emoji} New Patreon Post: [{title}]({url})"

def send_to_discord(post):

    content = format_discord_message(post)
    payload = {
        "username": DISCORD_BOTNAME,
        "content": content
        # No avatar_url provided — will use Discord's default
    }
    
    if DISCORD_BOT_AVATAR:
        payload["avatar_url"] = DISCORD_BOT_AVATAR

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
        print("Cached ids: ", cached_ids)
        print("Post IDs: ", [post['id'] for post in posts])
        print("Posts: ", posts)

        # Ensure we are comparing with the latest posts in the correct order
        
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
