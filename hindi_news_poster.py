import os
from datetime import datetime
from openai import OpenAI
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class HindiNewsPoster:
    def __init__(self):
        # OpenAI setup
        self.openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        # Facebook setup
        self.facebook_access_token = os.getenv('FACEBOOK_ACCESS_TOKEN')
        self.facebook_page_id = os.getenv('FACEBOOK_PAGE_ID')
    
    def get_hindi_news(self):
        """Fetch today's news in Hindi using OpenAI API"""
        today = datetime.now().strftime("%d %B %Y")
        
        prompt = f"""आप एक हिंदी समाचार संपादक हैं जो आज ({today}) की सबसे महत्वपूर्ण खबरों का सारांश तैयार करते हैं।

आज की प्रमुख खबरों का एक आकर्षक और जानकारीपूर्ण सारांश हिंदी में तैयार करें।

निम्नलिखित विषयों को कवर करें:
- 🇮🇳 राष्ट्रीय समाचार (भारत)
- 🌍 अंतर्राष्ट्ल समाचार
- 💼 व्यापार और अर्थव्यवस्था
- 🏏 खेल
- 🎬 मनोरंजन
- 🔬 विज्ञान और प्रौद्योगिकी
- 🏥 स्वास्थ्य

Facebook पोस्ट के लिए फॉर्मेट करें (300-400 शब्द)। शामिल करें:
- एक आकर्षक शीर्षक
- 4-6 प्रमुख समाचार बिंदु
- प्रत्येक खबर को संक्षिप्त और स्पष्ट रखें
- उपयुक्त इमोजी का उपयोग करें
- प्रासंगिक हैशटैग (#आजकीखबर #समाचार #भारत #ताजाखबर)

भाषा शुद्ध हिंदी में हो, सरल और समझने में आसान हो। पेशेवर लेकिन आकर्षक लहजा रखें।"""

        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "आप एक अनुभवी हिंदी समाचार संपादक हैं जो सोशल मीडिया के लिए आकर्षक और जानकारीपूर्ण सामग्री बनाते हैं।"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=800,
                temperature=0.7
            )
            
            news_content = response.choices[0].message.content.strip()
            return news_content
        
        except Exception as e:
            print(f"Error fetching Hindi news from OpenAI: {e}")
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
        """Main function to fetch Hindi news and post to Facebook"""
        print("📰 आज की हिंदी समाचार प्राप्त कर रहे हैं...")
        news_content = self.get_hindi_news()
        
        if not news_content:
            print("Failed to fetch Hindi news. Exiting.")
            return
        
        print("\n" + "="*50)
        print("Generated Hindi News Content:")
        print("="*50)
        print(news_content)
        print("="*50 + "\n")
        
        print("Posting to Facebook...")
        self.post_to_facebook(news_content)
        
        print("\n✓ Hindi news posting completed! 🎉")

if __name__ == "__main__":
    poster = HindiNewsPoster()
    poster.run()
