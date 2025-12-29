# Tech News Poster

Automatically fetch today's latest tech news using OpenAI GPT and post it to Twitter and/or LinkedIn.

## Features

- 🤖 Uses OpenAI GPT-4 to curate and summarize today's tech news
- 🐦 Posts to Twitter (optional)
- 💼 Posts to LinkedIn (optional)
- ⚙️ Configurable to post to one or both platforms
- 🔒 Secure credential management with environment variables

## Prerequisites

- Python 3.8 or higher
- OpenAI API key
- Twitter API credentials (if posting to Twitter)
- LinkedIn API credentials (if posting to LinkedIn)

## Installation

1. **Clone or download this repository**

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   - Copy `.env.example` to `.env`:
     ```bash
     copy .env.example .env
     ```
   - Edit `.env` and add your API credentials

## Getting API Credentials

### OpenAI API Key (Required)
1. Go to [OpenAI Platform](https://platform.openai.com/api-keys)
2. Sign in or create an account
3. Navigate to API Keys section
4. Create a new API key
5. Copy the key to your `.env` file

### Twitter API Credentials (Optional)
1. Go to [Twitter Developer Portal](https://developer.twitter.com/en/portal/dashboard)
2. Create a new app or use an existing one
3. Navigate to "Keys and tokens" section
4. Generate API Key, API Secret, Access Token, and Access Token Secret
5. Copy all credentials to your `.env` file

**Note:** You need **Elevated** access for Twitter API v2 to post tweets.

### LinkedIn API Credentials (Optional)
1. Go to [LinkedIn Developers](https://www.linkedin.com/developers/)
2. Create a new app
3. Request access to the "Share on LinkedIn" product
4. Generate an access token with `w_member_social` scope
5. Get your LinkedIn Person ID (member ID)
6. Copy credentials to your `.env` file

**Note:** LinkedIn API access requires app review for posting capabilities.

## Usage

### Post to both Twitter and LinkedIn:
```bash
python news_poster.py both
```

### Post to Twitter only:
```bash
python news_poster.py twitter
```

### Post to LinkedIn only:
```bash
python news_poster.py linkedin
```

### Default (no argument = both):
```bash
python news_poster.py
```

## Automation

### Schedule with Windows Task Scheduler:
1. Open Task Scheduler
2. Create a new task
3. Set trigger (e.g., daily at 9 AM)
4. Set action: Run `python.exe` with arguments:
   - Program: `C:\Path\To\Python\python.exe`
   - Arguments: `C:\Users\Rakesh_Kumar42\.windsurf\daily_news_poster\news_poster.py both`
   - Start in: `C:\Users\Rakesh_Kumar42\.windsurf\daily_news_poster`

### Schedule with cron (Linux/Mac):
```bash
# Edit crontab
crontab -e

# Add this line to run daily at 9 AM
0 9 * * * cd /path/to/daily_news_poster && python news_poster.py both
```

## How It Works

1. **Fetch News:** The script uses OpenAI's GPT-4 to generate a curated summary of today's tech news
2. **Format Content:** The news is formatted as an engaging social media post with hashtags
3. **Post:** The content is posted to your selected platform(s)

## Customization

You can modify the news generation prompt in `news_poster.py` to:
- Focus on specific tech topics
- Change the tone (more formal, casual, etc.)
- Adjust the length
- Add specific hashtags

Look for the `get_tech_news()` method in the `TechNewsPoster` class.

## Troubleshooting

### "Twitter credentials not configured"
- Ensure all Twitter credentials are in your `.env` file
- Verify you have Elevated access in Twitter Developer Portal

### "LinkedIn credentials not configured"
- Ensure LinkedIn access token and person ID are in your `.env` file
- Verify your app has "Share on LinkedIn" permissions

### "Error fetching news from OpenAI"
- Check your OpenAI API key is valid
- Ensure you have sufficient credits in your OpenAI account
- Verify your internet connection

## Security Notes

- Never commit your `.env` file to version control
- Keep your API keys secure and rotate them regularly
- The `.env` file is already in `.gitignore`

## License

MIT License - Feel free to use and modify as needed.

## Contributing

Feel free to submit issues or pull requests for improvements!
