from flask import Flask, request, jsonify
import os
import json

app = Flask(__name__)
# app.config['PREFERRED_URL_SCHEME'] = 'https'

# Define the path where data will be stored
DATA_DIR = "./data"
SECRETS_DIR = "./secrets"

@app.before_request
def before_request():
    if request.method in ['POST', 'PUT']:
        if not request.is_json:
            try:
                # Try to parse the request data as JSON
                request.json = request.get_json()
            except Exception as e:
                return jsonify({"error": "Invalid JSON data"}), 400

@app.route('/create/<bucket>', methods=['POST'])
def create_bucket(bucket):
    try:
        data = request.get_json()

        # Check if the request includes the necessary fields
        if "token" not in data or "password" not in data:
            return jsonify({"error": "Incomplete request data"}), 400

        # Validate the token against the tokens.txt file
        if not is_valid_token(data["token"]):
            return jsonify({"error": "Invalid token"}), 401

        # Create the user's bucket directory if it doesn't exist
        user_bucket_dir = os.path.join(DATA_DIR, bucket)
        os.makedirs(user_bucket_dir, exist_ok=True)

        # Save the user's password in a file within the bucket
        password_file = os.path.join(user_bucket_dir, "password.txt")
        with open(password_file, 'w') as file:
            file.write(data["password"])

        return jsonify({"message": "Bucket created successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/upload/<bucket>/<type>/<name>', methods=['POST','PUT'])
def upload_file(bucket, type, name):
    try:
        # Get the request data
        data = request.get_json()

        # Check if the request includes the necessary fields
        if "password" not in data or "data" not in data:
            return jsonify({"error": "Incomplete request data"}), 400

        # Validate the user's password
        if not is_valid_password(bucket, data["password"]):
            return jsonify({"error": "Invalid password"}), 401

        # Create the directory structure if it doesn't exist
        file_path = os.path.join(DATA_DIR, bucket, type)
        os.makedirs(file_path, exist_ok=True)

        # Define the file name based on the "name" field
        file_name = os.path.join(file_path, f"{name}.json")

        # Store the JSON data on the server
        with open(file_name, 'w') as file:
            json.dump(data["data"], file)

        return jsonify({"message": "File uploaded successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/<bucket>/<type>/<name>' , methods=['GET'])
def get_data(bucket, type, name):
    try:
        # Check the password
        password = request.args.get('auth')

        if not is_valid_password(bucket, password):
            return jsonify({"error": "Invalid password"}), 401

        file_name = os.path.join(DATA_DIR, bucket, type, f'{name}.json')
        with open(file_name, 'r') as file:
            data = json.load(file)

        return data, 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/<bucket>/all', methods=['GET'])
def get_all_data(bucket):
    try:
        password = request.args.get('auth')

        if not is_valid_password(bucket, password):
            return jsonify({"error": "Invalid password"}), 401

        # Construct the full path to the bucket directory
        bucket_path = os.path.join(DATA_DIR, bucket)

        # Compile all JSON data together and return
        
        # # List all JSON files in the bucket directory
        # json_files = [f for f in os.listdir(bucket_path) if f.endswith('.json')]

        # return jsonify({"files": json_files}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


def is_valid_token(token):
    # Check if the token exists in the tokens.txt file
    tokens_file_path = os.path.join(SECRETS_DIR, "tokens.txt")
    if not os.path.isfile(tokens_file_path):
        return False

    with open(tokens_file_path, 'r') as file:
        valid_tokens = [line.strip() for line in file.readlines()]

    return token in valid_tokens

def is_valid_password(bucket, password):
    # Check if the password exists in the user's password.txt file
    password_file_path = os.path.join(DATA_DIR, bucket, "password.txt")
    if not os.path.isfile(password_file_path):
        return False
    
    with open(password_file_path, 'r') as file:
        return password == file.readline()

if __name__ == '__main__':
    app.run(debug=True)
