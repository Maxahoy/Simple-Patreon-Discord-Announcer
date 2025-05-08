import requests
import os
import json

# Set your access token here or fetch it from an environment variable
ACCESS_TOKEN = os.getenv("PATREON_ACCESS_TOKEN")  # Set this in your environment
API_URL = "https://www.patreon.com/api/oauth2/v2/campaigns"


# Function to get campaign ID
def get_campaign_id():
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }
    response = requests.get(API_URL, headers=headers)
    
    if response.status_code == 200:
        # Parse the response to get the campaign ID
        data = response.json()
        campaign_id = data['data'][0]['id']  # Assuming there's one campaign
        print(f"Campaign ID: {campaign_id}")
        return campaign_id
    else:
        print(f"Error fetching campaign: {response.status_code}")
        print(response.text)
        return None


def fetch_latest_posts(campaign_id, limit=10):
    post_url = f"https://www.patreon.com/api/oauth2/v2/campaigns/{campaign_id}/posts"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }
    params = {
        "page[size]": 100,
        "fields[post]": "title,url,tiers,published_at"
    }

    all_posts = []
    cursor = None

    while len(all_posts) < limit:
        if cursor:
            params["page[cursor]"] = cursor

        response = requests.get(post_url, headers=headers, params=params)

        if response.status_code != 200:
            print(f"Error fetching posts: {response.status_code}")
            print(response.text)
            break

        data = response.json()
        posts = data.get("data", [])

        if not posts:
            print("No more posts found.")
            break

        all_posts.extend(posts)

        next_cursor_url = data.get("links", {}).get("next")
        if next_cursor_url:
            cursor_param = next_cursor_url.split("page%5Bcursor%5D=")[-1].split("&")[0]
            cursor = cursor_param
        else:
            break

    # Sort by published_at descending (newest first)
    sorted_posts = sorted(
        all_posts,
        key=lambda post: post['attributes']['published_at'],
        reverse=True
    )

    return sorted_posts[:limit]

def identify_tiers(posts):
    """
    Given a list of post objects, return a set of all unique tier IDs referenced in the posts.
    """
    tier_ids = set()
    for post in posts:
        tiers = post.get("attributes", {}).get("tiers", [])
        tier_ids.update(tiers)
    return tier_ids


def fetch_tier_metadata_from_campaign(campaign_id, target_tier_ids=None):
    """
    Fetch all tiers from the campaign and print details for the provided tier IDs.
    If target_tier_ids is None, prints all tiers.
    """
    url = f"https://www.patreon.com/api/oauth2/v2/campaigns/{campaign_id}"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }
    params = {
        "include": "tiers",
        "fields[tier]": "title,description,amount_cents"
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code != 200:
        print(f"Error fetching campaign tiers: {response.status_code}")
        print(response.text)
        return {}

    data = response.json()
    included = data.get("included", [])
    tier_details = {}

    for item in included:
        if item.get("type") != "tier":
            continue

        tier_id = int(item["id"])  # Convert to int for matching
        if target_tier_ids and tier_id not in target_tier_ids:
            continue

        attributes = item.get("attributes", {})
        title = attributes.get("title", "Unknown Title")
        description = attributes.get("description", "No description")
        amount_cents = attributes.get("amount_cents", 0)
        amount_usd = f"${amount_cents / 100:.2f}"

        tier_details[tier_id] = {
            "title": title,
            "description": description,
            "amount_usd": amount_usd
        }

        print(f"Tier ID: {tier_id}")
        print(f"  Title      : {title}")
        print(f"  Description: {description}")
        print(f"  Amount     : {amount_usd}")
        print()

    return tier_details


if __name__ == "__main__":
    campaign_id = get_campaign_id()
    if campaign_id:
        posts = fetch_latest_posts(campaign_id, limit=5)  # Fetch the last 5 posts
        tiers = identify_tiers(posts)
        print("Tier ID's: ", tiers)
        fetch_tier_metadata_from_campaign(campaign_id, tiers)