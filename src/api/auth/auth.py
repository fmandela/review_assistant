import os
import jwt
from datetime import datetime
from flask import Blueprint, jsonify, request


from src.data.mongodb_client import MongoDBClient

# Set the secret key for JWT token
SECRET_KEY = os.getenv('SECRET_KEY', 'SECRETKEYSHOULDBEINENV')

auth = Blueprint('auth', __name__, url_prefix='/api/auth')

client = MongoDBClient()

# Endpoint for getting a token


@auth.route('/get_token', methods=['POST'])
def get_token():
    app_name = request.json.get('app_name')
    public_key = request.json.get('public_key')
    platform = request.json.get('platform')

    app_doc = client.find_one('apps', {'app_name': app_name})
    if app_doc is None:
        client.insert_one('apps', {'app_name': app_name,
                          'public_key': public_key, 'platform': platform})
    elif app_doc['public_key'] != public_key or app_doc['platform'] != platform:
        return jsonify({'error': 'Invalid app credentials'}), 400

    token = jwt.encode({'app_name': app_name, 'platform': platform, 'created_at': str(
        datetime.now()), 'public_key': public_key}, SECRET_KEY, algorithm='HS256')
    return jsonify(
        {
            'status': 'Succeeded',
            'message': 'App registered successfully',
            'app_name': app_name,
            'token': token
        }
    )
