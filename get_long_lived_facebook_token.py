import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Your Facebook App credentials
APP_ID = "750090700854253"  # Your app ID
APP_SECRET = input("Enter your App Secret: ")  # Get from Facebook App Dashboard
SHORT_LIVED_TOKEN = os.getenv('FACEBOOK_ACCESS_TOKEN')  # Your current token

print("Step 1: Exchanging short-lived token for long-lived token...")

# Exchange short-lived token for long-lived user token (60 days)
url = "https://graph.facebook.com/v18.0/oauth/access_token"
params = {
    'grant_type': 'fb_exchange_token',
    'client_id': APP_ID,
    'client_secret': APP_SECRET,
    'fb_exchange_token': SHORT_LIVED_TOKEN
}

response = requests.get(url, params=params)
data = response.json()

if 'access_token' in data:
    long_lived_user_token = data['access_token']
    print(f"✓ Long-lived user token obtained (expires in {data.get('expires_in', 0)} seconds)")
    print(f"Long-lived user token: {long_lived_user_token[:50]}...")
    
    print("\nStep 2: Getting long-lived page token...")
    
    # Get page access token using long-lived user token
    url2 = "https://graph.facebook.com/v18.0/me/accounts"
    params2 = {'access_token': long_lived_user_token}
    
    response2 = requests.get(url2, params=params2)
    pages_data = response2.json()
    
    if 'data' in pages_data:
        print(f"\n✓ Found {len(pages_data['data'])} page(s):\n")
        
        for page in pages_data['data']:
            print(f"Page Name: {page['name']}")
            print(f"Page ID: {page['id']}")
            print(f"Long-Lived Page Access Token:")
            print(f"{page['access_token']}")
            print("-" * 80)
            
            # Check if this is your page
            if page['id'] == '905589205979351':
                print(f"\n✅ YOUR PAGE TOKEN (Never expires as long as app is active):")
                print(f"FACEBOOK_ACCESS_TOKEN={page['access_token']}")
                print("\nUpdate this token in your .env file!")
    else:
        print(f"Error getting pages: {pages_data}")
else:
    print(f"Error: {data}")
    print("\nMake sure:")
    print("1. Your App Secret is correct")
    print("2. Your current token is valid")
    print("3. You have the right permissions")
