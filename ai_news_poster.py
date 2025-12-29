import os
from datetime import datetime
from openai import OpenAI
import tweepy
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class AINewsPoster:
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
    
    def get_ai_ml_news(self):
        """Fetch today's AI/ML news using OpenAI API with exciting tone"""
        today = datetime.now().strftime("%B %d, %Y")
        
        prompt = f"""You are an enthusiastic AI/ML news curator who LOVES artificial intelligence and machine learning! 🚀

Generate an EXCITING and ENERGETIC summary of today's ({today}) most groundbreaking AI and Machine Learning news across the industry!

Focus EXCLUSIVELY on AI/ML topics including:
- 🤖 Large Language Models (LLMs) & Generative AI
- 🧠 Deep Learning breakthroughs
- 🔬 AI Research & Papers
- 💼 AI in Enterprise & Business
- 🎨 AI Art & Creative Tools
- 🏥 AI in Healthcare & Science
- 🚗 Autonomous Systems & Robotics
- 📊 MLOps & AI Infrastructure
- 🔐 AI Safety & Ethics
- 🌟 AI Startups & Funding
- 🏆 AI Competitions & Benchmarks

Write in an EXCITING, ENTHUSIASTIC tone that shows genuine passion for AI! Use:
- Emojis to add energy! 🔥💡✨
- Exclamation marks to show excitement!
- Words like "Amazing!", "Incredible!", "Game-changing!", "Revolutionary!"
- Make readers feel the HYPE and EXCITEMENT of AI innovation!

Format as an engaging LinkedIn post (can be longer than Twitter's limit). Include:
- A catchy opening line that grabs attention
- 3-5 major AI/ML stories with exciting descriptions
- Relevant hashtags (#AI #MachineLearning #DeepLearning #GenerativeAI #LLM #AINews)
- A closing line that builds anticipation for the future

Make it professional yet ENERGETIC - like you're sharing amazing news with friends who love AI as much as you do!"""

        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an enthusiastic AI/ML expert who creates exciting, engaging social media content about artificial intelligence and machine learning. You're passionate about AI and it shows in your writing!"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=800,
                temperature=0.8
            )
            
            news_content = response.choices[0].message.content.strip()
            return news_content
        
        except Exception as e:
            print(f"Error fetching AI news from OpenAI: {e}")
            return None
    
    def post_to_twitter(self, content):
        """Post content to Twitter"""
        if not self.twitter_client:
            print("Twitter credentials not configured. Skipping Twitter post.")
            return False
        
        try:
            # Twitter has 280 char limit, so truncate if needed
            if len(content) > 280:
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
        """Main function to fetch AI/ML news and post to selected platform(s)"""
        print("🤖 Fetching today's exciting AI/ML news...")
        news_content = self.get_ai_ml_news()
        
        if not news_content:
            print("Failed to fetch AI news. Exiting.")
            return
        
        print("\n" + "="*50)
        print("Generated AI/ML News Content:")
        print("="*50)
        print(news_content)
        print("="*50 + "\n")
        
        if platform.lower() in ['twitter', 'both']:
            print("Posting to Twitter...")
            self.post_to_twitter(news_content)
        
        if platform.lower() in ['linkedin', 'both']:
            print("Posting to LinkedIn...")
            self.post_to_linkedin(news_content)
        
        print("\n✓ AI News posting completed! 🚀")

if __name__ == "__main__":
    import sys
    
    # Get platform from command line argument (default: linkedin)
    platform = sys.argv[1] if len(sys.argv) > 1 else 'linkedin'
    
    if platform not in ['twitter', 'linkedin', 'both']:
        print("Usage: python ai_news_poster.py [twitter|linkedin|both]")
        sys.exit(1)
    
    poster = AINewsPoster()
    poster.run(platform)
