from flask import Flask, request
import requests
from datetime import datetime
import os
from urllib.parse import quote as url_quote  # Corrected import

app = Flask(__name__)

@app.route('/track', methods=['GET'])
def track():
    user_ip = request.remote_addr  # Get the user's IP address
    user_agent = request.headers.get('User-Agent')  # Get the user agent (browser info)
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Get geolocation data based on the IP
    location = get_geolocation(user_ip)

    # Log the request with IP, user-agent, and location
    log_request(user_ip, user_agent, timestamp, location)

    return "Tracking successful!", 200

def get_geolocation(ip):
    # You can use a service like ipinfo.io to get geolocation data
    try:
        response = requests.get(f'https://ipinfo.io/{ip}/json')
        data = response.json()
        return data.get('city', 'Unknown') + ', ' + data.get('country', 'Unknown')
    except Exception as e:
        return 'Error getting location'

def log_request(ip, user_agent, timestamp, location):
    # Save logs to a file
    with open("logs.txt", "a") as f:
        f.write(f"{timestamp} - IP: {ip}, User Agent: {user_agent}, Location: {location}\n")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
