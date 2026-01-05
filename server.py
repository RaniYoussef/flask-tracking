from flask import Flask, request
import requests
from datetime import datetime
import os

app = Flask(__name__)

# Route for the base URL ('/')
@app.route('/')
def home():
    # Get the user's IP address and user agent
    user_ip = request.remote_addr
    user_agent = request.headers.get('User-Agent')
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Get geolocation data based on IP
    location = get_geolocation(user_ip)

    # Log the request with IP, user-agent, and location
    log_request(user_ip, user_agent, timestamp, location)

    # Return the information directly in the response
    return f"Tracking successful!<br>IP: {user_ip}<br>User Agent: {user_agent}<br>Location: {location}<br>Timestamp: {timestamp}", 200

# Function to get geolocation information based on the user's IP
def get_geolocation(ip):
    try:
        response = requests.get(f'https://ipinfo.io/{ip}/json')
        data = response.json()
        # Return city and country
        return data.get('city', 'Unknown') + ', ' + data.get('country', 'Unknown')
    except Exception as e:
        return 'Error getting location'

# Function to log the request information
def log_request(ip, user_agent, timestamp, location):
    # Save the log details to a file
    with open("logs.txt", "a") as f:
        f.write(f"{timestamp} - IP: {ip}, User Agent: {user_agent}, Location: {location}\n")

# Run the Flask app (dynamic port for deployment)
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))  # Port 5000 for local testing
