# telegram_bot.py - Main bot file with MongoDB integration
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes
)
from config import BOT_TOKEN, TMDB_API_KEY, ADMIN_ID, MONGO_URI
from mongo_db import MongoDB
import requests
from datetime import datetime

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# TMDB API Configuration
TMDB_BASE_URL = "https://api.themoviedb.org/3"
TMDB_IMAGE_URL = "https://image.tmdb.org/t/p/w1280"

class MovieBot:
    def __init__(self):
        self.db = MongoDB(MONGO_URI)

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Send start message with buttons and track users"""
        user = update.effective_user
        chat = update.effective_chat
        
        # Track user/chat in database
        self.db.add_interaction(
            user_id=user.id,
            username=user.username or user.first_name,
            chat_id=chat.id,
            chat_type=chat.type,
            chat_title=chat.title if hasattr(chat, 'title') else None
        )
        
        keyboard = [
            [InlineKeyboardButton("🎬 Movies", callback_data='movies'),
             InlineKeyboardButton("📺 Series", callback_data='series')],
            [InlineKeyboardButton("🔥 Trending", callback_data='trending')]
        ]
        
        await update.message.reply_text(
            "🎥 *Movie/Series Poster Bot*\nSend me a name or use buttons:",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )

    async def handle_query(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle inline button presses"""
        query = update.callback_query
        await query.answer()

        if query.data in ['movies', 'series']:
            await query.edit_message_text(f"Send me a {query.data} name (e.g.: 'Inception' or 'Breaking Bad')")
        elif query.data == 'trending':
            await self.send_trending(update)

    async def send_poster(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Fetch and send landscape poster"""
        query = update.message.text
        try:
            params = {'api_key': TMDB_API_KEY, 'query': query}
            endpoint = 'movie' if 'movie' in query.lower() else 'tv'
            response = requests.get(f"{TMDB_BASE_URL}/search/{endpoint}", params=params).json()
            
            if response['results']:
                poster_path = response['results'][0]['backdrop_path']
                await update.message.reply_photo(f"{TMDB_IMAGE_URL}{poster_path}")
                # Track successful request
                self.db.increment_request(update.effective_user.id)
            else:
                await update.message.reply_text("❌ No results found")
        except Exception as e:
            logger.error(e)
            await update.message.reply_text("⚠️ Error fetching data")

    async def send_trending(self, update: Update) -> None:
        """Send trending content"""
        try:
            data = requests.get(
                f"{TMDB_BASE_URL}/trending/all/day",
                params={'api_key': TMDB_API_KEY}
            ).json()
            if data['results']:
                poster_path = data['results'][0]['backdrop_path']
                await update.callback_query.message.reply_photo(f"{TMDB_IMAGE_URL}{poster_path}")
        except Exception as e:
            logger.error(e)
            await update.callback_query.message.reply_text("⚠️ Trending fetch failed")

    async def show_stats(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Admin-only statistics command"""
        user = update.effective_user
        if user.id != ADMIN_ID:
            await update.message.reply_text("⛔ You don't have permission for this command.")
            return
            
        stats = self.db.get_stats()
        message = (
            f"📊 *Bot Statistics*\n\n"
            f"👤 Total Users: {stats['total_users']}\n"
            f"👥 Total Groups: {stats['total_groups']}\n"
            f"📨 Total Requests: {stats['total_requests']}\n"
            f"📅 Last 24h Active: {stats['active_last_24h']}\n\n"
            f"⏱ Last updated: {stats['timestamp']}"
        )
        await update.message.reply_text(message, parse_mode='Markdown')

def main():
    """Start the bot"""
    app = Application.builder().token(BOT_TOKEN).build()
    bot = MovieBot()

    # Handlers
    app.add_handler(CommandHandler('start', bot.start))
    app.add_handler(CommandHandler('stats', bot.show_stats))
    app.add_handler(CallbackQueryHandler(bot.handle_query))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, bot.send_poster))

    logger.info("Bot is running...")
    app.run_polling()

if __name__ == '__main__':
    main()
