import os
from flask import Flask, request
import requests

TELEGRAM_TOKEN = os.environ['TELEGRAM_BOT_TOKEN']
URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    chat_id = data["message"]["chat"]["id"]
    message = data["message"].get("text", "")

    reply = f"You said: {message}"

    requests.post(URL, json={
        "chat_id": chat_id,
        "text": reply
    })

    return "ok", 200

@app.route('/')
def home():
    return "Bot is live!", 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
