import requests
import json
import hashlib
from vbl_aquarium.models.dock import *

# # Define headers (if needed)
headers = {
    "Content-Type": "application/json"
}

def hash256(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Define the API endpoint URL
api_url = "http://localhost:5000/create/dan_bucket"

data = BucketModel(
    token = "c503675a-506c-48c0-9b5e-5265e8260a06",
    password = hash256("password")
)

print(hash256("password"))

response = requests.post(api_url, data=data.model_dump_json(), headers=headers)

# Check the response
if response.status_code == 201:
    print(response.text)
else:
    print("Error:", response.status_code, response.text)

# ## Create some real data

# api_url = f'http://localhost:5000/upload/dan_bucket/neuron/n1?auth={hash256("password")}'

# # # Define the data to be sent in the PUT request
# data = {
#     "data": {
#         "position": [1,2,3]
#     }
# }

# # # Convert the data to a JSON string
# json_data = json.dumps(data)

# # # Send the PUT request
# response = requests.put(api_url, data=json_data, headers=headers)

# # Check the response
# if response.status_code == 201:
#     print(response.text)
# else:
#     print("Error:", response.status_code, response.text)

# ## Get your data back

# api_url = f'http://localhost:5000/dan_bucket/neuron/n1?auth={hash256("password")}'

# response = requests.get(api_url)

# if response.status_code == 201:
#     print(response.text)
# else:
#     print("Error:", response.status_code, response.text)

