import werkzeug
from sqlalchemy.exc import SQLAlchemyError

from app import app

# =================== Handling Exceptions ==================


@app.errorhandler(ValueError)
def handle_value_error(error):
    return {"error": str(error)}, 400


@app.errorhandler(werkzeug.exceptions.UnsupportedMediaType)
def handle_unsupported_media_type_error(error):
    return {"error": "Unsupported media type. Please send JSON data."}, 415


@app.errorhandler(SQLAlchemyError)
def handle_database_error(error):
    return {"error": "Database error occurred"}, 500


@app.errorhandler(Exception)
def handle_global_error(error):
    return {"error": "Internal Server Error"}, 500
