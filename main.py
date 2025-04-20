from flask import Flask, request
import telegram
import os

TOKEN = os.environ['TELEGRAM_BOT_TOKEN']
bot = telegram.Bot(token=TOKEN)

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    chat_id = update.message.chat.id
    bot.send_message(chat_id=chat_id, text="Hello from Flask!")
    return "OK"

if __name__ == '__main__':
    app.run(host="100.20.92.101", port=5000)
