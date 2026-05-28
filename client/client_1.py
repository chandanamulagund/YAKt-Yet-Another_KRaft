import requests
import json
from constants import BROKER_HOST, BASE_URL

# Set the URL of your Flask server
url = f'{BASE_URL}/api/register-broker-record'

# Data to be sent in JSON format
data = {
  "internalUUID": 0,
  "brokerId": 0,
  "brokerHost":BROKER_HOST,
  "brokerPort": "9092",
  "securityProtocol": "https",
  "brokerStatus": "INIT",
  "rackId": "rack-1",
  "epoch": 0
}


# Set the headers to indicate that we're sending JSON
headers = {'Content-Type': 'application/json'}

# Send the POST request with JSON data
response = requests.post(url, data=json.dumps(data), headers=headers)

# Print the response from the server
print("Response from server:")
print(response.status_code)  # HTTP status code
print(response.text)  # Response body
