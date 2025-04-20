import os
import requests
from datetime import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

API_KEY = os.environ['MY_OPEN_WEATHER_MAP_API_KEY']

# Convert country code to flag emoji
def get_flag_emoji(country_code):
    return chr(0x1F1E6 + ord(country_code[0].upper()) - ord('A')) + chr(0x1F1E6 + ord(country_code[1].upper()) - ord('A'))


def get_weather(location):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={API_KEY}&units=metric"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        city = data['name']
        country = data['sys']['country']
        country_flag = get_flag_emoji(country)
        temp = data['main']['temp']
        feels_like = data['main']['feels_like']
        desc = data['weather'][0]['description']
        humidity = data['main']['humidity']
        pressure = data['main']['pressure']
        wind_speed = data['wind']['speed']
        wind_deg = data['wind'].get('deg', 'N/A')

        # Convert sunrise/sunset to local time using timezone offset
        timezone_offset = data.get('timezone', 0)
        utc_offset_hours = timezone_offset // 3600
        utc_offset_str = f"UTC{'+' if utc_offset_hours >= 0 else ''}{utc_offset_hours}"

        sunrise_ts = data['sys']['sunrise'] + timezone_offset
        sunset_ts = data['sys']['sunset'] + timezone_offset

        sunrise = datetime.utcfromtimestamp(sunrise_ts).strftime('%H:%M')
        sunset = datetime.utcfromtimestamp(sunset_ts).strftime('%H:%M')

        emoji = weather_emoji(desc)
        desc_translated = weather_translate(desc)

        return (f"{city}, {country} {country_flag}:\n"
                f"🌡️ Temperatura:  {temp}°C (Seziliwi: {feels_like}°C)\n"
                f"ℹ️ Jaǵday:  {desc_translated.capitalize()} {emoji}\n"
                f"💧 Iǵallıq:  {humidity}%\n"
                f"📈 Basım:  {pressure} hPa\n"
                f"🌬️ Samal tezligi:  {wind_speed} m/s, {wind_deg}°\n"
                f"🌅 Quyash shıǵıw waqtı:  {sunrise} ({utc_offset_str})\n"
                f"🌇 Quyash batıw waqtı:  {sunset} ({utc_offset_str})")
    else:
        return "😔 Bul jerdi taba almadım. Qaytadan jiberiń."


# Add emojis based on keywords in the description
def weather_emoji(description):
    description = description.lower()
    if "clear" in description:
        return "☀️"
    elif "cloud" in description:
        return "☁️"
    elif "rain" in description:
        return "🌧️"
    elif "thunder" in description:
        return "⛈️"
    elif "snow" in description:
        return "❄️"
    elif "fog" in description or "mist" in description:
        return "🌫️"
    else:
        return "🌍"


def weather_translate(description):
    description = description.lower()
    if "clear" in description:
        return "quyashlı"
    elif "cloud" in description:
        return "bulıtlı"
    elif "rain" in description:
        return "jawınlı"
    elif "thunder" in description:
        return "shaqmaqlı"
    elif "snow" in description:
        return "qarlı"
    elif "fog" in description or "mist" in description:
        return "dumanlı"
    else:
        return "🌍"


# /start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Qalanıń atın jiberiń. Hawa-rayı haqqıda maǵlımat beremen!")


# Message handler
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    location = update.message.text  # Get location directly from the message
    weather_info = get_weather(location)
    await update.message.reply_text(weather_info)


if __name__ == "__main__":
    TELEGRAM_TOKEN = os.environ['TELEGRAM_BOT_TOKEN']
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot is running...")
    app.run_polling()  # You can optionally specify a polling interval here if needed
    # app.run_polling(poll_interval=1, timeout=30)
