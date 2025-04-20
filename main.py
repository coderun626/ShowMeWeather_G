from flask import Flask, request
import requests
import os

TOKEN = os.environ['TELEGRAM_BOT_TOKEN']
URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    chat_id = data["message"]["chat"]["id"]
    requests.post(URL, json={
        "chat_id": chat_id,
        "text": "Hello from Flask!"
    })
    return "OK"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
