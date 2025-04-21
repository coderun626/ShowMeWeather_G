from flask import Flask, request
import requests
import os
from datetime import datetime

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
        weather = data['weather'][0]
        wind = data['wind']
        sys = data['sys']
        
        temp = main['temp']
        feels_like = main['feels_like']
        desc = weather['description']
        humidity = main['humidity']
        pressure = main['pressure']
        wind_speed = wind['speed']
        wind_deg = wind['deg']
        sunrise = datetime.utcfromtimestamp(sys['sunrise']).strftime('%H:%M:%S')
        sunset = datetime.utcfromtimestamp(sys['sunset']).strftime('%H:%M:%S')

        return (f"🌡️ Temp: {temp}°C (Feels like {feels_like}°C)\n"
                f"☁️ Condition: {desc.capitalize()}\n"
                f"💧 Humidity: {humidity}%\n"
                f"📈 Pressure: {pressure} hPa\n"
                f"🌬️ Wind: {wind_speed} m/s, {wind_deg}°\n"
                f"🌅 Sunrise: {sunrise}\n"
                f"🌇 Sunset: {sunset}")
    else:
        return "Sorry, I couldn't retrieve the weather information."

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    chat_id = data["message"]["chat"]["id"]
    message_text = data["message"]["text"]
    
    # Remove leading/trailing whitespaces
    city_name = message_text.strip()

    if city_name:
        weather_info = get_weather(city_name)
    else:
        weather_info = "Please provide a city name."

    requests.post(URL, json={
        "chat_id": chat_id,
        "text": weather_info
    })
    
    return "OK"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
