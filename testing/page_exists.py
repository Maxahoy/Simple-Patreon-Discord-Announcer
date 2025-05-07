import requests
from bs4 import BeautifulSoup

url = 'https://www.patreon.com/TestingMyDiscordBot'  # Replace with the creator's page URL
response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    posts = soup.find_all('article')  # Assuming the posts are within <article> tags
    print(f"Found {len(posts)} posts.")
else:
    print("Error fetching page:", response.status_code)
