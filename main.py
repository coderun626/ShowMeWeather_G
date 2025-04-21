from flask import Flask, request
import requests
import os

TOKEN = os.environ['TELEGRAM_BOT_TOKEN']
URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
WEATHER_API_KEY = os.environ['WEATHER_API_KEY']
WEATHER_API_URL = "http://api.openweathermap.org/data/2.5/weather"

app = Flask(__name__)

def get_weather(city_name):
    params = {
        'q': city_name,
        'appid': WEATHER_API_KEY,
        'units': 'metric',  # For temperature in Celsius
        'lang': 'en'  # For English language responses
    }
    response = requests.get(WEATHER_API_URL, params=params)
    data = response.json()
    
    if response.status_code == 200:
        main = data['main']
        weather_description = data['weather'][0]['description']
        temp = main['temp']
        return f"The weather in {city_name} is {weather_description} with a temperature of {temp}°C."
    else:
        return "Sorry, I couldn't retrieve the weather information."

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    chat_id = data["message"]["chat"]["id"]
    message_text = data["message"]["text"]
    
    # Remove leading/trailing whitespaces and check if the message starts with 'weather in'
    message_text = message_text.strip().lower()
    
    if message_text.startswith('weather in'):
        city_name = message_text[len('weather in '):].strip()
        if city_name:
            weather_info = get_weather(city_name)
        else:
            weather_info = "Please provide a city name after 'weather in'."
    else:
        weather_info = "Hello! Send a city name in the format 'weather in [city]' to get the weather."

    requests.post(URL, json={
        "chat_id": chat_id,
        "text": weather_info
    })
    
    return "OK"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
