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

# Function to fetch the latest post (only the most recent post)
def fetch_latest_post(campaign_id):
    post_url = f"https://www.patreon.com/api/oauth2/v2/campaigns/{campaign_id}/posts"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }
    params = {
        "page[size]": 1,  # Fetch only the most recent post
        "fields[post]":"title,url"
    }
    # Build the request
    req = requests.Request("GET", post_url, headers=headers, params=params)
    prepared = req.prepare()

    # Print final URL
    print("Request URL:", prepared.url)
    print("Request Headers:", prepared.headers)
    response = requests.get(post_url, headers=headers, params=params)
    
    if response.status_code == 200:
        posts = response.json()
        
        # Check if the data contains posts
        if posts['data']:
            
            latest_post = posts['data'][0]  # Grab the first (and only) post
            print(latest_post)
            post_id = latest_post.get('id', 'No ID available')
            attributes = latest_post.get('attributes', {})
            title = attributes.get('title', 'No title available')
            url = attributes.get('url', 'No URL available')
            
            # Print the post title and URL
            print(f"Post ID: {post_id}")
            print(f"Title: {title}")
            print(f"URL: {url}")
        else:
            print("No posts found.")
    else:
        print(f"Error fetching posts: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    campaign_id = get_campaign_id()
    if campaign_id:
        fetch_latest_post(campaign_id)
