from flask import Flask, request
import requests
from datetime import datetime
import os
from urllib.parse import quote as url_quote  # Corrected import

app = Flask(__name__)

# Route for tracking the image access
@app.route('/track', methods=['GET'])
def track():
    user_ip = request.remote_addr  # Get the user's IP address
    user_agent = request.headers.get('User-Agent')  # Get the user agent (browser info)
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Get geolocation data based on IP
    location = get_geolocation(user_ip)

    # Log the request with IP, user-agent, and location
    log_request(user_ip, user_agent, timestamp, location)

    return "Tracking successful!", 200

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

# Run the Flask app
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
