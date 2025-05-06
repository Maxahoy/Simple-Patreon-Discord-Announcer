import requests
from bs4 import BeautifulSoup
import os
from pathlib import Path

# === CONFIGURATION ===
CREATOR_USERNAME = "TestingMyDiscordBot"
WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")
LAST_POST_FILE = "last_post.txt"

PATRON_FEED_URL = f"https://www.patreon.com/{CREATOR_USERNAME}/posts"

def get_last_post_id():
    try:
        return Path(LAST_POST_FILE).read_text().strip()
    except FileNotFoundError:
        return None

def set_last_post_id(post_id):
    Path(LAST_POST_FILE).write_text(post_id)

def get_latest_post():
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; PatreonBot/1.0)",
    }
    response = requests.get(PATRON_FEED_URL, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    # Find the first post title link
    post_link = soup.select_one('a[data-tag="post-title"]')
    if not post_link:
        raise RuntimeError("No posts found.")

    href = post_link.get("href")
    title = post_link.text.strip()

    if not href.startswith("/posts/"):
        raise RuntimeError("Unexpected post URL format.")

    post_id = href.split("/")[-1]
    full_url = f"https://www.patreon.com{href}"

    return post_id, title, full_url

def send_to_discord(title, url):
    payload = {
        "content": f"🆕 New Patreon post: **{title}**\n{url}"
    }
    response = requests.post(WEBHOOK_URL, json=payload)
    response.raise_for_status()

def main():
    last_post_id = get_last_post_id()
    try:
        post_id, title, url = get_latest_post()
    except Exception as e:
        print(f"Error fetching post: {e}")
        return

    if post_id != last_post_id:
        print(f"New post detected: {title}")
        send_to_discord(title, url)
        set_last_post_id(post_id)
    else:
        print("No new post.")

if __name__ == "__main__":
    main()
