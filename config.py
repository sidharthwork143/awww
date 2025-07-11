# config.py
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get config values
BOT_TOKEN = os.getenv("BOT_TOKEN")  # Your bot token from BotFather
TMDB_API_KEY = os.getenv("TMDB_API_KEY")  # Your TMDB API key
ADMIN_ID = int(os.getenv('ADMIN_ID'))  # Your Telegram user ID
MONGO_URI = os.getenv("MONGO_URI")  # Your MongoDB URI

# Debugging: Print values to ensure they are loaded correctly
print("BOT_TOKEN:", BOT_TOKEN)  # Remove this line after debugging
print("ADMIN_ID:", ADMIN_ID)  # Remove this line after debugging
