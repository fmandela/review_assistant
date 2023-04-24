import logging
import os
from flask import Flask, Response, jsonify, request
import yaml
from flask_swagger_ui import get_swaggerui_blueprint


from src.utils.utils import validate_app_token
from src.api.auth.auth import auth
from src.api.errors import errors
from src.api.reviews.reviews import reviews

if os.environ.get('ENV') == 'development':
    logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

SECRET_KEY = os.getenv('SECRET_KEY', 'SECRETKEYSHOULDBEINENV')
PUBLIC_KEY = os.getenv('PUBLIC_KEY', 'PUBLICKKEYIN')


@app.errorhandler(404)
def page_not_found(e):
    return jsonify({"message": "Not Found"}), 404


@app.errorhandler(405)
def page_not_found(e):
    return jsonify({'message': 'Bad Request'}), 405


@app.errorhandler(500)
def server_error(e):
    return jsonify({'message': 'Internal server error'}), 500


def generate_swagger_spec():
    with open('src/docs/swagger.yaml') as file:
        swag = yaml.load(file, Loader=yaml.FullLoader)

    return swag


@app.route('/swagger.json', methods=['GET'])
def swagger_spec():
    swag = generate_swagger_spec()
    return jsonify(swag)


def create_swagger_ui_blueprint():
    swagger_ui_blueprint = get_swaggerui_blueprint(
        '/docs',
        '/swagger.json',
        config={
            'app_name': 'Review Assistant'
        }
    )
    return swagger_ui_blueprint


@app.before_request
def protect_endpoints():
    #     logging.debug(f'Request received: {request.method} {request.path}')

    # Ignore requests to the get_token endpoint
    if request.path.startswith('/api/auth/') or request.path == '/' or request.path.startswith('/docs') or request.path.startswith('/swagger.json'):
        return

    if request.method not in ['GET', 'POST', 'PUT', 'DELETE']:
        return jsonify({'message': 'Invalid request method'}), 405

    if request.method == 'POST' and request.json is None:
        return jsonify({'message': 'POST request without a body'}), 400

    # Check if Authorization header exists
    if 'Authorization' not in request.headers:
        return jsonify({'message': 'Authorization header is missing'}), 401

    # Check if Authorization header starts with Bearer
    auth_header = request.headers.get('Authorization')
    if not auth_header.startswith('Bearer'):
        return jsonify({'message': 'Invalid Authorization header'}), 401

    # Extract the token from the Authorization header
    token = auth_header.split(' ')[1]

    # Call the validate_token function to verify the token
    if not validate_app_token(token):
        return jsonify({'message': 'Invalid token'}), 401


app.register_blueprint(auth)
app.register_blueprint(errors)
app.register_blueprint(reviews)
app.register_error_handler(400, page_not_found)
app.register_blueprint(create_swagger_ui_blueprint())


@app.route('/', methods=['GET'])
def index():
    return jsonify(
        {
            'name': 'Review Assistant',
            'documentation': 'https://' + request.host + '/docs'
        }
    ), 200


@app.route('/health', methods=['GET'])
def health():
    return Response('OK', status=200)
