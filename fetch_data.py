"""
This script is adapted from a code snippet originally shared on Xiaohongshu.
I have modified the request logic, error handling, pagination, and file structure
to fit the needs of this project. The script is intended for educational purposes only.
"""

import httpx
import json
import os
import time

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Safari/605.1.15",
    "Cookie": "YOUR COOKIE HERE", # replace with your own if running locally
}

base_url = "https://www.ssense.com/en-jp/women/clothing.json"
os.makedirs("ssense_json", exist_ok=True)

res = httpx.get(f"{base_url}?page=1", headers=headers, timeout=10.0, verify=False, follow_redirects=True)
if "application/json" not in res.headers.get("Content-Type", ""):
    print("Failed to get JSON on page 1")
    print("Preview:", res.text[:300])
    exit()

data = res.json()
#total_pages = data["pagination_info"]["totalPages"]
total_pages = 27 # enough for this particular assignment
print(f"Total pages: {total_pages}")

for page in range(1, total_pages + 1):
    url = f"{base_url}?page={page}"
    res = httpx.get(url, headers=headers, timeout=10.0, verify=False, follow_redirects=True)


    if res.status_code != 200:
        print(f"Page {page} failed with status {res.status_code}")
        continue

    try:
        products = res.json()["products"]
    except Exception as e:
        print(f"Page {page} JSON decode error:", e)
        continue

    save_name = f"ssense_json/page_{page}.json"
    with open(save_name, "w", encoding="utf-8") as f:
        json.dump(products, f, indent=4, ensure_ascii=False)

    print(f"Saved page {page}")
    time.sleep(5)