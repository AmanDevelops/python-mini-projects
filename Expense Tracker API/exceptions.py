import werkzeug

from app import app


@app.errorhandler(werkzeug.exceptions.UnsupportedMediaType)
@app.errorhandler(werkzeug.exceptions.BadRequest)
def handle_no_json_error(error):
    return {"message": "Unsupported Media Type, require application/json"}, 400


@app.errorhandler(ValueError)
def invalid_input_error(error):
    return {"message": str(error)}, 400
