import os
import json

CACHE_FILE = "recent_posts.json"

def flush_cache():
    if os.path.exists(CACHE_FILE):
        os.remove(CACHE_FILE)
        print(f"✅ Cache file '{CACHE_FILE}' deleted.")
    else:
        print(f"ℹ️ No cache file '{CACHE_FILE}' found to delete.")

if __name__ == "__main__":
    flush_cache()
