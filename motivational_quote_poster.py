import os
from datetime import datetime
from openai import OpenAI
import tweepy
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class MotivationalQuotePoster:
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
    
    def get_motivational_quote(self):
        """Generate inspiring motivational quote using OpenAI API"""
        today = datetime.now().strftime("%A, %B %d, %Y")
        
        prompt = f"""You are a motivational speaker and life coach who inspires people to achieve their dreams and overcome challenges.

Create an INSPIRING and UPLIFTING motivational post for {today} that will energize and motivate people to take action!

Your post should:
- Start with a powerful, attention-grabbing opening
- Include an inspiring quote (either famous or original)
- Add a brief reflection or call-to-action that encourages readers
- Use emojis strategically to enhance the emotional impact ✨💪🌟🔥💡
- Be authentic, genuine, and heartfelt
- Focus on themes like:
  * Personal growth and self-improvement
  * Overcoming obstacles and resilience
  * Pursuing dreams and goals
  * Positive mindset and gratitude
  * Success and achievement
  * Inner strength and confidence
  * Taking action and making changes
  * Believing in yourself

Format for LinkedIn (can be 200-300 words). Include:
- A compelling opening line
- The main inspirational quote (formatted beautifully)
- A personal reflection or story element
- A motivating call-to-action
- Relevant hashtags (#Motivation #Inspiration #Success #Growth #Mindset #BelieveInYourself)

Make it feel personal, authentic, and genuinely inspiring - like a friend sharing wisdom that changed their life!"""

        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an inspiring motivational speaker who creates authentic, heartfelt content that genuinely helps people feel empowered and motivated. Your words have the power to change lives."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=600,
                temperature=0.9
            )
            
            quote_content = response.choices[0].message.content.strip()
            return quote_content
        
        except Exception as e:
            print(f"Error generating motivational quote from OpenAI: {e}")
            return None
    
    def post_to_twitter(self, content):
        """Post content to Twitter"""
        if not self.twitter_client:
            print("Twitter credentials not configured. Skipping Twitter post.")
            return False
        
        try:
            # Twitter has 280 char limit, so truncate if needed
            if len(content) > 280:
                # Try to find a good breaking point
                content = content[:277] + "..."
            
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
        """Main function to generate and post motivational quote"""
        print("✨ Generating today's motivational quote...")
        quote_content = self.get_motivational_quote()
        
        if not quote_content:
            print("Failed to generate motivational quote. Exiting.")
            return
        
        print("\n" + "="*50)
        print("Generated Motivational Content:")
        print("="*50)
        print(quote_content)
        print("="*50 + "\n")
        
        if platform.lower() in ['twitter', 'both']:
            print("Posting to Twitter...")
            self.post_to_twitter(quote_content)
        
        if platform.lower() in ['linkedin', 'both']:
            print("Posting to LinkedIn...")
            self.post_to_linkedin(quote_content)
        
        print("\n✓ Motivational quote posted successfully! 💪✨")

if __name__ == "__main__":
    import sys
    
    # Get platform from command line argument (default: linkedin)
    platform = sys.argv[1] if len(sys.argv) > 1 else 'linkedin'
    
    if platform not in ['twitter', 'linkedin', 'both']:
        print("Usage: python motivational_quote_poster.py [twitter|linkedin|both]")
        sys.exit(1)
    
    poster = MotivationalQuotePoster()
    poster.run(platform)
