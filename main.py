from flask import Flask, request
import requests
import os

TOKEN = os.environ['TELEGRAM_BOT_TOKEN']
URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
MY_OPEN_WEATHER_MAP_API_KEY = os.environ['MY_OPEN_WEATHER_MAP_API_KEY']
WEATHER_API_URL = "http://api.openweathermap.org/data/2.5/weather"

app = Flask(__name__)

def get_weather(city_name):
    params = {
        'q': city_name,
        'appid': MY_OPEN_WEATHER_MAP_API_KEY,
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
    
    # Check if the message starts with a location request
    if message_text.lower().startswith('weather in'):
        city_name = message_text[len('weather in '):].strip()
        weather_info = get_weather(city_name)
        response_text = weather_info
    else:
        response_text = "Hello! Send a city name to get the weather."

    requests.post(URL, json={
        "chat_id": chat_id,
        "text": response_text
    })
    
    return "OK"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
