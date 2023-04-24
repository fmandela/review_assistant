import os
import jwt
from datetime import datetime, timedelta
from src.data.mongodb_client import MongoDBClient


# Set the secret key for JWT token
SECRET_KEY = os.getenv('SECRET_KEY', 'SECRETKEYSHOULDBEINENV')

client = MongoDBClient()


def validate_app_token(token):
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        app_name = decoded_token['app_name']
        platform = decoded_token['platform']
        public_key = decoded_token['public_key']
        created_at_str = decoded_token['created_at']
        created_at = datetime.fromisoformat(created_at_str)

        # check if the token has expired (last login was more than 24 hours ago)
        if datetime.now() - created_at > timedelta(hours=24):
            return False

        if client.find_one('apps', {'app_name': app_name, 'platform': platform, 'public_key': public_key}):
            return True
    except:
        pass
    return False
