# config.py - Configuration with MongoDB support
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

BOT_TOKEN = os.getenv("6007398311:AAF1s-_khhR6fQmJRRPdU0DsDaSvhEP9TH8")  # From @BotFather
TMDB_API_KEY = os.getenv("http://www.omdbapi.com/?i=tt3896198&apikey=a956c290")  # From themoviedb.org
ADMIN_ID = int(os.getenv("1960614875"))  # Your Telegram user ID
MONGO_URI = os.getenv("mongodb+srv://sidharthwork143:fn6HFQ2ErnAT7ggT@cluster0.umwqqcl.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")  # mongodb://localhost:27017 or Atlas URI
