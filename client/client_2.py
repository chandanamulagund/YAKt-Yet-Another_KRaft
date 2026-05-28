import requests
import json
from constants import BASE_URL

# Set the URL of your Flask server
url = f'{BASE_URL}/api/topic-record'

# Data to be sent in JSON format
data = {
    "topicUUID": 0,
    "name": "name_01"
}


# Set the headers to indicate that we're sending JSON
headers = {'Content-Type': 'application/json'}

# Send the POST request with JSON data
response = requests.post(url, data=json.dumps(data), headers=headers)

# Print the response from the server
print("Response from server:")
print(response.status_code)  # HTTP status code
print(response.text)  # Response body
