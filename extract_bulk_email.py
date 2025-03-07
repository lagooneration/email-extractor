import requests

api_key = "your_hunter_api_key"
domain = "harvard.edu"  # Example domain

response = requests.get(f"https://api.hunter.io/v2/domain-search?domain={domain}&api_key={api_key}")
data = response.json()

if "data" in data:
    emails = [item["value"] for item in data["data"]["emails"]]
    print(emails)
