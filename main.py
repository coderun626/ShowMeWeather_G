from flask import Flask, request
import requests
import os
from datetime import datetime
import pytz

TOKEN = os.environ['TELEGRAM_BOT_TOKEN']
URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
WEATHER_API_KEY = os.environ['WEATHER_API_KEY']
WEATHER_API_URL = "http://api.openweathermap.org/data/2.5/weather"

app = Flask(__name__)

# Emoji flags by country code
COUNTRY_FLAGS = {
    "US": "🇺🇸", "GB": "🇬🇧", "IN": "🇮🇳", "CA": "🇨🇦", "AU": "🇦🇺", 
    "FR": "🇫🇷", "DE": "🇩🇪", "ES": "🇪🇸", "IT": "🇮🇹", "BR": "🇧🇷",
    "RU": "🇷🇺", "JP": "🇯🇵", "MX": "🇲🇽", "CN": "🇨🇳", "ZA": "🇿🇦"
    # Add more countries as needed
}

def convert_to_local_time(utc_timestamp, timezone_offset):
    """
    Converts a UTC timestamp to local time based on the timezone offset.
    timezone_offset is in seconds (e.g., -18000 for UTC-5).
    """
    utc_time = datetime.utcfromtimestamp(utc_timestamp)
    local_time = utc_time + timedelta(seconds=timezone_offset)
    return local_time.strftime('%H:%M:%S')

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
        sunrise_utc = sys['sunrise']
        sunset_utc = sys['sunset']
        
        # Get the country code and find the flag emoji
        country_code = sys['country']
        flag = COUNTRY_FLAGS.get(country_code, "🏳️")  # Default flag if not found

        # Get the timezone offset (in seconds)
        timezone_offset = data['timezone']

        # Convert sunrise and sunset to local time using the timezone offset
        sunrise_local = convert_to_local_time(sunrise_utc, timezone_offset)
        sunset_local = convert_to_local_time(sunset_utc, timezone_offset)

        city_country = f"{city_name}, {country_code} {flag}"

        return (f"🌍 {city_country}\n"
            f"🌡️ Temp: {temp}°C (Feels like {feels_like}°C)\n"
            f"☁️ Condition: {desc.capitalize()}\n"
            f"💧 Humidity: {humidity}%\n"
            f"📈 Pressure: {pressure} hPa\n"
            f"🌬️ Wind: {wind_speed} m/s, {wind_deg}°\n"
            f"🌅 Sunrise: {sunrise_local} (Local) / {datetime.utcfromtimestamp(sunrise_utc).strftime('%H:%M:%S')} (UTC)\n"
            f"🌇 Sunset: {sunset_local} (Local) / {datetime.utcfromtimestamp(sunset_utc).strftime('%H:%M:%S')} (UTC)")

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
