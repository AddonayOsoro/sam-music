import requests
import os

API_KEY = "Sbv90crb4zF3gbd0SdCEMZtKWZyDaE67j8OUz5MX7o4Tx3g0PrZ3NtFb"
headers = {"Authorization": API_KEY}

url = "https://api.pexels.com/v1/search"
params = {
    "query": "nature",  
    "per_page": 150,  
    "page": 1,  
}

response = requests.get(url, headers=headers, params=params)
data = response.json()

if not os.path.exists("images"):
    os.makedirs("images")

for photo in data["photos"]:
    image_url = photo["src"]["large"]
    image_response = requests.get(image_url)
    image_name = os.path.join("images", f"{photo['id']}.jpg")
    with open(image_name, "wb") as f:
        f.write(image_response.content)

print("Images downloaded successfully.")
