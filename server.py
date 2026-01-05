from flask import Flask, request, redirect, url_for
import requests
from datetime import datetime
import os

app = Flask(__name__)

# Route for the fake tracking link that will redirect the user
@app.route('/track-and-redirect', methods=['GET'])
def track_and_redirect():
    # Extract the destination URL from the query parameter
    destination_url = request.args.get('destination')

    if not destination_url:
        return "No destination URL provided.", 400

    # Get the user's IP and user agent
    user_ip = request.remote_addr
    user_agent = request.headers.get('User-Agent')
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Get the geolocation based on the user's IP
    location = get_geolocation(user_ip)

    # Log the request details
    log_request(user_ip, user_agent, timestamp, location)

    # Redirect the user to the real destination URL
    return redirect(destination_url)

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
