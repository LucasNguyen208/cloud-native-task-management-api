from flask import jsonify

from app.errors.exceptions import APIError


def register_error_handlers(app):

    @app.errorhandler(APIError)
    def handle_api_error(error):

        return (jsonify({"message": error.message}), error.status_code)
