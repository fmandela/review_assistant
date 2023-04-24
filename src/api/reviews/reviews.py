import os
from flask import Blueprint, jsonify, request

from src.assistant.assistant import Assistant

reviews = Blueprint('reviews', __name__, url_prefix='/api/reviews')

assistant = Assistant()


@reviews.route('/', methods=['GET'])
def get_reviews():
    data = request.get_json()
    # validate the request data
    if not data:
        return jsonify({'error': 'No review data found'}), 400
    try:
        response = assistant.respond(prompt=data['comments'])

        return jsonify({'review': response}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
