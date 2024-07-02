
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Function to get the location and temperature
def get_location_and_temperature(ip):
    # Example IP Geolocation API (free but might require registration for an API key)
    ip_info_url = f"http://ipinfo.io/{ip}/json"
    response = requests.get(ip_info_url)
    data = response.json()


    city = data.get('city', 'New York')

    weather_api_key = '6eac1c3b94b30c0a0658661b8e02c2c9:'
    weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_key}&units=metric"
    weather_response = requests.get(weather_url)
    weather_data = weather_response.json()

    # Extract temperature
    temperature = weather_data['main']['temp'] if 'main' in weather_data else '11'

    return city, temperature

@app.route('/')
def hello():
    visitor_name = request.args.get('visitor_name', 'Guest')

    # Get the client's IP address
    client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)

    # Get the location and temperature based on IP
    city, temperature = get_location_and_temperature(client_ip)

    # Create the response
    response = {
        "client_ip": client_ip,
        "location": city,
        "greeting": f"Hello, {visitor_name}!, the temperature is {temperature} degrees Celsius in {city}"
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)

