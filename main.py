
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await update.message.reply_text("Hello! I'm alive bro!")
    except Exception as e:
        print(f"Error in start command: {e}")

def main():
    try:
        token = os.environ.get("BOT_TOKEN")
        if not token:
            raise ValueError("BOT_TOKEN environment variable is not set")
        
        app = ApplicationBuilder().token(token).build()
        app.add_handler(CommandHandler("start", start))
        
        print("Bot is running...")
        app.run_polling()
    except Exception as e:
        print(f"Error starting bot: {e}")

if __name__ == "__main__":
    main()
