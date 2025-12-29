import os
import requests
from dotenv import load_dotenv

load_dotenv()

access_token = os.getenv('LINKEDIN_ACCESS_TOKEN')

# Try userinfo endpoint
url = "https://api.linkedin.com/v2/userinfo"
headers = {
    "Authorization": f"Bearer {access_token}"
}

response = requests.get(url, headers=headers)
print("UserInfo Response:")
print(response.json())

# Try me endpoint
url2 = "https://api.linkedin.com/v2/me"
response2 = requests.get(url2, headers=headers)
print("\nMe Response:")
print(response2.json())