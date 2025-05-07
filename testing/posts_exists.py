import requests
import os

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


# Function to fetch the latest posts (fetches multiple posts)
def fetch_latest_posts(campaign_id, limit=5):
    post_url = f"https://www.patreon.com/api/oauth2/v2/campaigns/{campaign_id}/posts"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }
    params = {
        "page[size]": limit,  # Fetch the last 'limit' posts
        "fields[post]": "title,url,tiers",  # Get post title, url, and tiers
    }
    
    response = requests.get(post_url, headers=headers, params=params)
    
    if response.status_code == 200:
        posts = response.json()
        
        # Check if the data contains posts
        if posts['data']:
            print(f"Found {len(posts['data'])} posts.")
            for latest_post in posts['data']:
                post_id = latest_post.get('id', 'No ID available')
                attributes = latest_post.get('attributes', {})
                title = attributes.get('title', 'No title available')
                url = attributes.get('url', 'No URL available')
                tiers = attributes.get('tiers', [])

                # Print the post title and URL
                print(f"\nPost ID: {post_id}")
                print(f"Title: {title}")
                print(f"URL: {url}")
                
                # Now, let's fetch the details for each tier
                if tiers:
                    print("Fetching tier details...")
                    fetch_tier_details(tiers)
                else:
                    print("No tiers associated with this post.")
        else:
            print("No posts found.")
    else:
        print(f"Error fetching posts: {response.status_code}")
        print(response.text)


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
        fetch_latest_posts(campaign_id, limit=5)  # Fetch the last 5 posts
