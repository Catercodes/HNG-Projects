from flask import Flask, request, jsonify
import requests
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

# Load API keys from environment variables
LOCATION_API_KEY = os.getenv('LOCATION_API_KEY')
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')

@app.route('/')
def index():
    return "Welcome to my Flask API!"

@app.route('/api/location', methods=['GET'])
def get_location_and_weather():
    client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)

    # Example coordinates for testing
    latitude, longitude = 40.730610, -73.935242

    # Get location data using Google Geocoding API
    location_url = f'https://maps.googleapis.com/maps/api/geocode/json?key={LOCATION_API_KEY}&latlng={latitude},{longitude}'
    location_response = requests.get(location_url)
    location_data = location_response.json()

    if location_data['status'] == 'OK':
        results = location_data['results'][0]
        city = None
        for component in results['address_components']:
            if 'locality' in component['types']:
                city = component['long_name']
                break
        city = city or 'Unknown City'
    else:
        city = 'Unknown City'
        latitude, longitude = 0.0, 0.0

    # Get weather data from OpenWeatherMap
    weather_url = f'https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={WEATHER_API_KEY}&units=metric'
    weather_response = requests.get(weather_url)
    weather_data = weather_response.json()

    temperature = weather_data.get('main', {}).get('temp', 'N/A')

    greeting = f"Hello, Mark!, the temperature is {temperature} degrees Celsius in {city}"

    return jsonify({
        "client_ip": client_ip,
        "location": city,
        "greeting": greeting
    })

if __name__ == '__main__':
    app.run(debug=True)
