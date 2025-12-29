import os
from datetime import datetime
from openai import OpenAI
import tweepy
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class TechNewsPoster:
    def __init__(self):
        # OpenAI setup
        self.openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        # Twitter setup
        self.twitter_client = None
        if all([os.getenv('TWITTER_API_KEY'), os.getenv('TWITTER_API_SECRET'),
                os.getenv('TWITTER_ACCESS_TOKEN'), os.getenv('TWITTER_ACCESS_SECRET')]):
            self.twitter_client = tweepy.Client(
                consumer_key=os.getenv('TWITTER_API_KEY'),
                consumer_secret=os.getenv('TWITTER_API_SECRET'),
                access_token=os.getenv('TWITTER_ACCESS_TOKEN'),
                access_token_secret=os.getenv('TWITTER_ACCESS_SECRET')
            )
        
        # LinkedIn setup
        self.linkedin_access_token = os.getenv('LINKEDIN_ACCESS_TOKEN')
        self.linkedin_person_id = os.getenv('LINKEDIN_PERSON_ID')
    
    def get_tech_news(self):
        """Fetch today's tech news using OpenAI API"""
        today = datetime.now().strftime("%B %d, %Y")
        
        prompt = f"""You are a tech news curator. Generate a concise, engaging summary of today's ({today}) most important technology news.

Include 3-5 key tech stories covering areas like:
- AI and Machine Learning
- Software Development
- Tech Companies
- Cybersecurity
- Innovation and Startups

Format the response as a social media post (under 280 characters for Twitter compatibility) that is informative and engaging. Include relevant hashtags.

Make it professional yet conversational."""

        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a professional tech news curator who creates engaging social media content."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            news_content = response.choices[0].message.content.strip()
            return news_content
        
        except Exception as e:
            print(f"Error fetching news from OpenAI: {e}")
            return None
    
    def post_to_twitter(self, content):
        """Post content to Twitter"""
        if not self.twitter_client:
            print("Twitter credentials not configured. Skipping Twitter post.")
            return False
        
        try:
            response = self.twitter_client.create_tweet(text=content)
            print(f"✓ Successfully posted to Twitter! Tweet ID: {response.data['id']}")
            return True
        except Exception as e:
            print(f"Error posting to Twitter: {e}")
            return False
    
    def post_to_linkedin(self, content):
        """Post content to LinkedIn"""
        if not self.linkedin_access_token or not self.linkedin_person_id:
            print("LinkedIn credentials not configured. Skipping LinkedIn post.")
            return False
        
        url = "https://api.linkedin.com/v2/ugcPosts"
        
        headers = {
            "Authorization": f"Bearer {self.linkedin_access_token}",
            "Content-Type": "application/json",
            "X-Restli-Protocol-Version": "2.0.0"
        }
        
        post_data = {
            "author": f"urn:li:person:{self.linkedin_person_id}",
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {
                        "text": content
                    },
                    "shareMediaCategory": "NONE"
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
            }
        }
        
        try:
            response = requests.post(url, headers=headers, json=post_data)
            if response.status_code == 201:
                print("✓ Successfully posted to LinkedIn!")
                return True
            else:
                print(f"Error posting to LinkedIn: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"Error posting to LinkedIn: {e}")
            return False
    
    def run(self, platform='both'):
        """Main function to fetch news and post to selected platform(s)"""
        print("Fetching today's tech news...")
        news_content = self.get_tech_news()
        
        if not news_content:
            print("Failed to fetch news. Exiting.")
            return
        
        print("\n" + "="*50)
        print("Generated Content:")
        print("="*50)
        print(news_content)
        print("="*50 + "\n")
        
        if platform.lower() in ['twitter', 'both']:
            print("Posting to Twitter...")
            self.post_to_twitter(news_content)
        
        if platform.lower() in ['linkedin', 'both']:
            print("Posting to LinkedIn...")
            self.post_to_linkedin(news_content)
        
        print("\n✓ Process completed!")

if __name__ == "__main__":
    import sys
    
    # Get platform from command line argument (default: both)
    platform = sys.argv[1] if len(sys.argv) > 1 else 'both'
    
    if platform not in ['twitter', 'linkedin', 'both']:
        print("Usage: python news_poster.py [twitter|linkedin|both]")
        sys.exit(1)
    
    poster = TechNewsPoster()
    poster.run(platform)
