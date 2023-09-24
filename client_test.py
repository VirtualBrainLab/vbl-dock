import requests
import json
import hashlib

# # Define headers (if needed)
headers = {
    "Content-Type": "application/json"
}

def hash256(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Define the API endpoint URL
api_url = "http://localhost:5000/create/dan_bucket"

# First create a new bucket
data = {
    "token": "c503675a-506c-48c0-9b5e-5265e8260a06",
    "password": hash256("password")
}

json_data = json.dumps(data)

response = requests.post(api_url, data=json_data, headers=headers)

# Check the response
if response.status_code == 201:
    print(response.text)
else:
    print("Error:", response.status_code, response.text)

## Create some real data

api_url = "http://localhost:5000/upload/dan_bucket/neuron/n1"

# # Define the data to be sent in the PUT request
data = {
    "password": hash256("password"),  # Replace with a hashed password
    "data": {
        "position": [1,2,3]
    }
}

# # Convert the data to a JSON string
json_data = json.dumps(data)

# # Send the PUT request
response = requests.put(api_url, data=json_data, headers=headers)

# Check the response
if response.status_code == 201:
    print(response.text)
else:
    print("Error:", response.status_code, response.text)
