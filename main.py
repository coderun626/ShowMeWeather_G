import os
import asyncio
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

API_KEY = os.environ['MY_OPEN_WEATHER_MAP_API_KEY']
TELEGRAM_TOKEN = os.environ['TELEGRAM_BOT_TOKEN']

flask_app = Flask(__name__)
telegram_app = None  # Global placeholder

# Fake weather (placeholder)
def get_weather(location):
    return f"Weather info for {location}"

# Telegram bot handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Send me a location name to get the weather!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    location = update.message.text
    weather_info = get_weather(location)
    await update.message.reply_text(weather_info)

@flask_app.route('/webhook', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), telegram_app.bot)
    asyncio.run(telegram_app.process_update(update))  # Run async function in sync Flask
    return "ok", 200

@flask_app.route('/')
def home():
    return "Bot is live!", 200

def create_app():
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    return application

if __name__ == '__main__':
    telegram_app = create_app()
    flask_app.run(host='0.0.0.0', port=5000)
