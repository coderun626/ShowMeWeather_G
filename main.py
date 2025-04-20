import os
import requests


def get_weather(location):
    # Replace 'YOUR_API_KEY' with your actual OpenWeatherMap API key
    api_key = os.environ['YOUR_API_KEY']
    url = f'http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric'

    # Send GET request to OpenWeatherMap API
    response = requests.get(url)

    # If the location is valid
    if response.status_code == 200:
        data = response.json()

        # Extract weather information
        city = data['name']
        temperature = data['main']['temp']
        weather_description = data['weather'][0]['description']
        humidity = data['main']['humidity']

        # Print the weather info
        print(f"Weather in {city}:")
        print(f"Temperature: {temperature}°C")
        print(f"Description: {weather_description.capitalize()}")
        print(f"Humidity: {humidity}%")
    else:
        print("Invalid location, please try again.")


if __name__ == "__main__":
    location = input("Enter location: ")  # Get location from the user
    get_weather(location)
