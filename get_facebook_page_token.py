import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Your current token (might be user token or app token)
current_token = os.getenv('FACEBOOK_ACCESS_TOKEN')

print("Attempting to get your Facebook Page Access Token...")
print(f"Current token: {current_token[:50]}...")

# Try to get pages you manage
url = "https://graph.facebook.com/v18.0/me/accounts"
params = {'access_token': current_token}

try:
    response = requests.get(url, params=params)
    data = response.json()
    
    if 'error' in data:
        print(f"\nError: {data['error']['message']}")
        print("\nYour current token cannot access pages. You need a User Access Token first.")
        print("\nSteps to get the correct token:")
        print("1. Go to: https://developers.facebook.com/tools/explorer/")
        print("2. Select your app")
        print("3. Click 'Generate Access Token'")
        print("4. Add permissions: pages_show_list, pages_read_engagement, pages_manage_posts")
        print("5. Generate token and run this script again")
    else:
        pages = data.get('data', [])
        if not pages:
            print("\nNo pages found. Make sure you're an admin of a Facebook Page.")
        else:
            print(f"\nFound {len(pages)} page(s):\n")
            for page in pages:
                print(f"Page Name: {page['name']}")
                print(f"Page ID: {page['id']}")
                print(f"Page Access Token: {page['access_token']}")
                print(f"Category: {page.get('category', 'N/A')}")
                print("-" * 80)
                
                # Check if this is your page
                if page['id'] == '905589205979351':
                    print(f"\n✓ Found your page! Use this token in your .env file:")
                    print(f"FACEBOOK_ACCESS_TOKEN={page['access_token']}")
                    
except Exception as e:
    print(f"Error: {e}")
