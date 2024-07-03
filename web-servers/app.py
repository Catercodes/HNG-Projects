from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

# Free APIs for geolocation and weather data
GEOLOCATION_API_URL = "http://ip-api.com/json/"
WEATHER_API_URL = "http://api.openweathermap.org/data/2.5/weather"
WEATHER_API_KEY = "6eac1c3b94b30c0a0658661b8e02c2c9"  # Replace with your OpenWeatherMap API key

@app.route('/')
def index():
    return "Welcome to the GeoIP and Weather API. Use the /api/hello endpoint with the visitor_name parameter."


def get_geolocation(ip):
    if ip == '127.0.0.1':
        ip ='8.8.8.8'

    response = requests.get(GEOLOCATION_API_URL + ip)
    return response.json()

def get_weather(city):
    params = {
        'q': city,
        'appid': WEATHER_API_KEY,
        'units': 'metric'  # Get temperature in Celsius
    }
    response = requests.get(WEATHER_API_URL, params=params)
    return response.json()

@app.route('/api/hello', methods=['GET'])
def hello():
    visitor_name = request.args.get('visitor_name', 'Unknown')
    
    # Get client's IP address
    client_ip = request.remote_addr

    # Get geolocation information
    geo_info = get_geolocation(client_ip)
    city = geo_info.get('city', 'Unknown')

    # Get weather information
    weather_info = get_weather(city)
    temperature = weather_info['main']['temp'] if 'main' in weather_info else 'Unknown'

    greeting = f"Hello, {visitor_name}!, the temperature is {temperature} degrees Celsius in {city}"

    response = {
        "client_ip": client_ip,
        "location": city,
        "greeting": greeting
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)