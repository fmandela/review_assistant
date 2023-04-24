from flask import Blueprint, Response, jsonify

errors = Blueprint("errors", __name__)


@errors.app_errorhandler(Exception)
def server_error(error):
    return Response(f"Oops, got an error! {error}", status=500)


@errors.errorhandler(Exception)
def handle_unexpected_error(e):
    return jsonify({'message': 'Unexpected error'}), 500

# @errors.errorhandler(Exception)
# def handle_unexpected_error(e):
#     if ENV == 'development':
#         return jsonify({'message': 'Unexpected error', 'error': str(e)}), 500
#     else:
#         return jsonify({'message': 'Unexpected error'}), 500
