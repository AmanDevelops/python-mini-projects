from flask import Flask

from auth.routes import auth_bp
from exceptions import AppException

app = Flask(__name__)


@app.errorhandler(AppException)
def handle_app_exception(error):
    response = {"error": error.message}
    return response, error.status_code


app.register_blueprint(auth_bp)
