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


# Function to fetch tier details by tier IDs
def fetch_tier_details(tier_ids):
    tier_url = "https://www.patreon.com/api/oauth2/v2/tiers"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }
    tier_names = []
    
    # Fetch tier details for each tier ID
    for tier_id in tier_ids:
        params = {
            "filter[id]": tier_id,
            "fields[tier]": "title",  # Only fetch tier title
        }
        
        response = requests.get(tier_url, headers=headers, params=params)
        
        if response.status_code == 200:
            tiers = response.json()
            
            if tiers['data']:
                tier = tiers['data'][0]  # Get the first (and only) tier
                tier_name = tier.get('attributes', {}).get('title', 'Unknown Tier')
                tier_names.append(tier_name)
            else:
                print(f"No data found for tier ID {tier_id}")
        else:
            print(f"Error fetching tier {tier_id}: {response.status_code}")
            print(response.text)
    
    if tier_names:
        print("Tiers associated with this post:")
        for tier_name in tier_names:
            print(f" - {tier_name}")
    else:
        print("No tiers found.")


if __name__ == "__main__":
    campaign_id = get_campaign_id()
    if campaign_id:
        posts = fetch_latest_posts(campaign_id, limit=5)  # Fetch the last 5 posts
        print(posts)