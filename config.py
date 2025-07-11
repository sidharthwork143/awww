# config.py - Configuration with MongoDB support
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")  # From @BotFather
TMDB_API_KEY = os.getenv("TMDB_API_KEY")  # From themoviedb.org
ADMIN_ID = int(os.getenv("ADMIN_ID"))  # Your Telegram user ID
MONGO_URI = os.getenv("MONGO_URI")  # mongodb://localhost:27017 or Atlas URI
