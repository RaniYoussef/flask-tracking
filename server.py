from flask import Flask, request
import requests
from datetime import datetime
import os

app = Flask(__name__)

@app.route('/track', methods=['GET'])
def track():
    user_ip = request.remote_addr
    user_agent = request.headers.get('User-Agent')
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Get geolocation data based on IP
    location = get_geolocation(user_ip)

    log_request(user_ip, user_agent, timestamp, location)

    return "Tracking successful!", 200

def get_geolocation(ip):
    try:
        response = requests.get(f'https://ipinfo.io/{ip}/json')
        data = response.json()
        return data.get('city', 'Unknown') + ', ' + data.get('country', 'Unknown')
    except Exception as e:
        return 'Error getting location'

def log_request(ip, user_agent, timestamp, location):
    with open("logs.txt", "a") as f:
        f.write(f"{timestamp} - IP: {ip}, User Agent: {user_agent}, Location: {location}\n")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
