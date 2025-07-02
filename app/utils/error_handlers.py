from flask import jsonify
from werkzeug.exceptions import HTTPException
from marshmallow import ValidationError
import logging

logger = logging.getLogger()

def register_error_handlers(app):
    @app.errorhandler(HTTPException)
    def handle_http_error(e):
        logger.warning(HTTPException)
        return jsonify({"error": e.description}), e.code

    @app.errorhandler(ValidationError)
    def handle_validation_error(e):
        logger.warning(f"ValidationError: {e.message}")
        return jsonify({"errors": e.message}), 400

    @app.errorhandler(Exception)
    def handle_generic_error(e):
        logger.exception("Unexpected error occurred")
        return jsonify({"error": "Внутренняя ошибка сервера"}), 500
