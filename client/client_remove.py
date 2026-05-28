import requests
import json
from constants import BROKER_HOST, BASE_URL

# Set the URL of your Flask server
url = f'{BASE_URL}/api/remove_node'

# Data to be sent in JSON format
data = {
    "node1": {"ip": BROKER_HOST, "port": "5566"}}

# Set the headers to indicate that we're sending JSON
headers = {'Content-Type': 'application/json'}

# Send the POST request with JSON data
response = requests.post(url, data=json.dumps(data), headers=headers)

# Print the response from the server
print("Response from server:")
print(response.status_code)  # HTTP status code
print(response.text)  # Response body
