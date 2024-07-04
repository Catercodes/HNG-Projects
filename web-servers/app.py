from flask import Flask, jsonify, request
import requests
import os

app = Flask(__name__)

# Free APIs for geolocation and weather data
GEOLOCATION_API_URL = "http://ip-api.com/json/"
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')  # Replace with your OpenWeatherMap API key

WEATHER_API_URL = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q=city"

@app.route('/')
def index():
    return "Welcome to the GeoIP and Weather API. Use the /api/hello endpoint with the visitor_name parameter."


def get_geolocation(ip):
    if ip == '127.0.0.1':
        ip ='8.8.8.8'

    response = requests.get(GEOLOCATION_API_URL + ip)
    if response is None:
        return
    data = response.json()
    return data['city']

def get_weather(city):
    #params = {
    #   'q': city,
    #    'appid': WEATHER_API_KEY,
    #    'units': 'metric'  # Get temperature in Celsius
    #}
    response = requests.get(f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={city}")
    if response is None:
        return None
    data = response.json()
    current = data.get('current')
    return current['temp_c']

@app.route('/api/hello', methods=['GET'])
def hello():
    visitor_name = request.args.get('visitor_name', 'Unknown')
    
    # Get client's IP address
    client_ip = request.remote_addr

    # Get geolocation information
    city = get_geolocation(client_ip)
    #city = geo_info.get('city', 'Unknown')

    # Get weather information
    #weather_info = get_weather(city)
    temperature = get_weather(city)
    #temperature = weather_info['main']['temp'] if 'main' in weather_info else 'Unknown'

    greeting = f"Hello, {visitor_name}!, the temperature is {temperature} degrees Celsius in {city}"

    response = {
        "client_ip": client_ip,
        "location": city,
        "greeting": greeting
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
