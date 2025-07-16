from concurrent.futures import ThreadPoolExecutor

from flask import Flask, Response, g
from redis import ConnectionPool, Redis

from auth.routes import auth_bp
from config import *
from database import Session, init_db
from exceptions import AppException
from exceptions.custom_exceptions import UrlNotFoundError
from service.models import Urls
from service.routes import url_bp

executor = ThreadPoolExecutor(max_workers=10)


init_db()

app = Flask(__name__)

redis_pool = ConnectionPool(
    host=REDIS_HOST,
    port=REDIS_PORT,
    password=REDIS_PASSWORD,
    db=0,
    max_connections=20,
    socket_connect_timeout=5,
    socket_timeout=5,
    retry_on_timeout=True,
)


@app.before_request
def setup_database():
    """Setup the database"""
    g.r = Redis(connection_pool=redis_pool)


@app.errorhandler(AppException)
def handle_app_exception(error):
    response = {"error": error.message}
    return response, error.status_code


app.register_blueprint(auth_bp)
app.register_blueprint(url_bp)


@app.route("/<string:short_code>", methods=["GET"])
def get_url_info(short_code):
    cached_url = g.r.get(short_code)
    if cached_url:
        response_data = Response(None, 302, {"Location": cached_url.decode()})
        executor.submit(update_views, short_code)
        return response_data

    with Session() as session:
        db_url_data = session.query(Urls).filter_by(short_code=short_code).first()
        if not db_url_data:
            raise UrlNotFoundError

        g.r.set(short_code, db_url_data.url, ex=10)
        db_url_data.views += 1
        executor.submit(update_views, short_code)

        response_data = Response(None, 302, {"Location": db_url_data.url})
        return response_data


def update_views(short_code):
    with Session() as thread_session:
        db_url_data = (
            thread_session.query(Urls).filter_by(short_code=short_code).first()
        )
        if db_url_data:
            db_url_data.views += 1
            thread_session.commit()
