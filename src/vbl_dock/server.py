from flask import Flask, request, jsonify
import os
import json
from vbl_aquarium.models.dock import BucketRequest, UploadRequest, LoadModel

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
        
        bucket_data = BucketRequest(**request.get_json())

        # Validate the token against the tokens.txt file
        if not is_valid_token(bucket_data.token):
            return jsonify({"error": "Invalid token"}), 401
        

        # Create the user's bucket directory if it doesn't exist
        user_bucket_dir = os.path.join(DATA_DIR, bucket)
        password_file = os.path.join(user_bucket_dir, "password.txt")

        if os.path.exists(user_bucket_dir) and os.path.exists(password_file):
            return jsonify({"error": "Bucket already exists"}), 409  
        
        os.makedirs(user_bucket_dir, exist_ok=True)

        # Save the user's password in a file within the bucket
        with open(password_file, 'w') as file:
            file.write(bucket_data.password)

        return jsonify({"message": "Bucket created successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/upload/<bucket>', methods=['POST','PUT'])
def upload_file(bucket):
    try:
        # Get the request data
        data = UploadRequest(**request.get_json())

        print(data.to_string())

        # Validate the user's password
        if not is_valid_password(bucket, data.password):
            return jsonify({"error": "Invalid password"}), 401

        # Create the directory structure if it doesn't exist
        bucket_path = os.path.join(DATA_DIR, bucket)

        # Define the file name based on the "name" field
        file_name = os.path.join(bucket_path, f"{data.type}.json")

        # Store the JSON data on the server
        with open(file_name, 'w') as file:
            file.write(data.data)

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

        files = os.listdir(bucket_path)

        types = []
        datas = []
        for file in files:
            if (file.endswith('.json')):
                type = file.split('.')[0]
                with open(os.path.join(bucket_path, file), 'r') as file:
                    raw = file.read()
                
                types.append(type)
                datas.append(raw)

        # Compile all JSON data together and return
        data = LoadModel(
            types=types,
            data=datas
        )
        
        return data.to_string(), 200

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
