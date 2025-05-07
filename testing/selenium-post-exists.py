from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Set up Chrome options for headless browsing
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Run in headless mode (no UI)
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# Set up the WebDriver using webdriver-manager to automatically manage ChromeDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# The URL of the Patreon creator's page (replace with the actual URL)
url = "https://www.patreon.com/TestingMyDiscordBot"

# Open the URL with the WebDriver
driver.get(url)

# Wait for JavaScript content to load (you can adjust the sleep time or use WebDriverWait for better control)
time.sleep(5)  # You can also try WebDriverWait for better performance

# Find all posts (you need to inspect the page to find the correct CSS selector for posts)
# Here's an example where we're looking for post titles; adjust the CSS selector based on actual structure
posts = driver.find_elements(By.CSS_SELECTOR, ".post-title-selector")  # Replace this with the actual selector

# Check if posts are found
if posts:
    print(f"Found {len(posts)} posts!")
    # Print titles of the posts
    for post in posts:
        print(post.text)
else:
    print("No posts found!")

# Clean up and close the browser
driver.quit()
