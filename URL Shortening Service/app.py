from flask import Flask, Response

from auth.routes import auth_bp
from database import Session, init_db
from exceptions import AppException
from exceptions.custom_exceptions import UrlNotFoundError
from service.models import Urls
from service.routes import url_bp

init_db()

app = Flask(__name__)


@app.errorhandler(AppException)
def handle_app_exception(error):
    response = {"error": error.message}
    return response, error.status_code


app.register_blueprint(auth_bp)
app.register_blueprint(url_bp)


@app.route("/<string:short_code>", methods=["GET"])
def get_url_info(short_code):
    with Session() as session:
        db_url_data = session.query(Urls).filter_by(short_code=short_code).first()
        if not db_url_data:
            raise UrlNotFoundError

        db_url_data.views += 1
        session.commit()

        response_data = Response(None, 302, {"Location": db_url_data.url})
        return response_data
