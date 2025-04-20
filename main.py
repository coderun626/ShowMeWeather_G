import os
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

API_KEY = os.environ['MY_OPEN_WEATHER_MAP_API_KEY']
TELEGRAM_TOKEN = os.environ['TELEGRAM_BOT_TOKEN']

# Flask app setup
flask_app = Flask(__name__)

# Weather API function (simplified version)
def get_weather(location):
    # Placeholder for weather response (replace with your actual API call)
    return f"Weather info for {location}"

# Telegram bot command and message handlers
def start(update: Update, context):
    update.message.reply_text("👋 Send me a location name to get the weather!")

def handle_message(update: Update, context):
    location = update.message.text
    weather_info = get_weather(location)
    update.message.reply_text(weather_info)

# Webhook route for Telegram
@flask_app.route('/webhook', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), telegram_app.bot)
    telegram_app.process_update(update)
    return "ok", 200

# Home route (just to verify app is live)
@flask_app.route('/')
def home():
    return "Bot is live!", 200

# Function to create the Telegram app and handlers
def create_app():
    telegram_app = Application.builder().token(TELEGRAM_TOKEN).build()
    telegram_app.add_handler(CommandHandler("start", start))
    telegram_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    return telegram_app

if __name__ == '__main__':
    # Create the Telegram app
    telegram_app = create_app()

    # Start the Flask server
    flask_app.run(host='0.0.0.0', port=5000)
