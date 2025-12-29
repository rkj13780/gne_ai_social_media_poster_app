import os
from datetime import datetime
from openai import OpenAI
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class IndianMotivationalQuotes:
    def __init__(self):
        # OpenAI setup
        self.openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        # Facebook setup
        self.facebook_access_token = os.getenv('FACEBOOK_ACCESS_TOKEN')
        self.facebook_page_id = os.getenv('FACEBOOK_PAGE_ID')
    
    def get_indian_motivational_quote(self):
        """Generate Indian-themed motivational quote using OpenAI API"""
        today = datetime.now().strftime("%A, %B %d, %Y")
        
        prompt = f"""You are an inspiring motivational speaker who draws wisdom from Indian culture, philosophy, and values to inspire youth and people of all ages.

Create a powerful, INSPIRING motivational post for {today} that resonates with Indian values and culture!

Your post should:
- Draw inspiration from Indian philosophy (Vedanta, Bhagavad Gita, Upanishads, etc.)
- Include quotes from Indian leaders, thinkers, or create original ones inspired by Indian wisdom
- Reference Indian values like:
  * Dharma (righteousness and duty)
  * Karma (action and its consequences)
  * Perseverance and resilience
  * Unity in diversity
  * Respect for knowledge and teachers (Guru-Shishya tradition)
  * Family and community values
  * Self-discipline and inner strength
- Speak to Indian youth and their aspirations
- Address modern challenges while staying rooted in timeless wisdom
- Use emojis strategically 🇮🇳✨💪🌟🔥💡🙏

Format for Facebook (200-300 words). Include:
- A powerful opening line
- An inspiring quote (from Indian leaders like Gandhi, Vivekananda, APJ Abdul Kalam, or original wisdom)
- Personal reflection connecting ancient wisdom to modern life
- Call-to-action that motivates youth to take action
- Relevant hashtags (#Motivation #IndianYouth #Inspiration #BharatKiShaan #YouthPower #IndianWisdom #Success)

Make it authentic, culturally rooted, and genuinely inspiring - like wisdom passed down from a mentor who understands both Indian values and modern aspirations!

Write in English but feel free to use Hindi words/phrases where they add authenticity (with English translation if needed)."""

        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an inspiring motivational speaker deeply rooted in Indian culture and philosophy. You create authentic content that resonates with Indian youth while honoring timeless wisdom from Indian traditions."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=700,
                temperature=0.9
            )
            
            quote_content = response.choices[0].message.content.strip()
            return quote_content
        
        except Exception as e:
            print(f"Error generating Indian motivational quote from OpenAI: {e}")
            return None
    
    def post_to_facebook(self, content):
        """Post content to Facebook Page"""
        if not self.facebook_access_token or not self.facebook_page_id:
            print("Facebook credentials not configured. Skipping Facebook post.")
            print("\nTo configure Facebook:")
            print("1. Go to https://developers.facebook.com/")
            print("2. Create an app and get Page Access Token")
            print("3. Add FACEBOOK_ACCESS_TOKEN and FACEBOOK_PAGE_ID to .env file")
            return False
        
        url = f"https://graph.facebook.com/v18.0/{self.facebook_page_id}/feed"
        
        payload = {
            'message': content,
            'access_token': self.facebook_access_token
        }
        
        try:
            response = requests.post(url, data=payload)
            
            if response.status_code == 200:
                result = response.json()
                print(f"✓ Successfully posted to Facebook! Post ID: {result.get('id')}")
                return True
            else:
                print(f"Error posting to Facebook: {response.status_code}")
                print(f"Response: {response.text}")
                return False
        except Exception as e:
            print(f"Error posting to Facebook: {e}")
            return False
    
    def run(self):
        """Main function to generate and post Indian motivational quote"""
        print("🇮🇳 Generating Indian motivational quote to inspire youth...")
        quote_content = self.get_indian_motivational_quote()
        
        if not quote_content:
            print("Failed to generate motivational quote. Exiting.")
            return
        
        print("\n" + "="*50)
        print("Generated Indian Motivational Content:")
        print("="*50)
        print(quote_content)
        print("="*50 + "\n")
        
        print("Posting to Facebook...")
        self.post_to_facebook(quote_content)
        
        print("\n✓ Indian motivational quote posted successfully! 🙏✨")

if __name__ == "__main__":
    poster = IndianMotivationalQuotes()
    poster.run()
