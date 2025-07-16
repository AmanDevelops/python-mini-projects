import uuid

from flask import Blueprint, request

from auth.handlers import auth_required
from database import Session
from exceptions.custom_exceptions import InvalidInputError, UrlNotFoundError
from service.models import Urls
from service.schemas import CreateUrl, CreateUrlResponse, UpdateUrl

url_bp = Blueprint("url", __name__, url_prefix="/shorten")


@url_bp.route("/", methods=["POST"])
@auth_required
def create_short_url(username):
    try:
        url_data = CreateUrl.model_validate_json(request.data)
    except:
        raise InvalidInputError

    with Session() as session:
        new_url = Urls(
            url=url_data.url, short_code=str(uuid.uuid4()), created_by_id=username
        )
        session.add(new_url)
        session.commit()
        session.refresh(new_url)
        response = CreateUrlResponse(
            id=new_url.id,
            url=new_url.url,
            short_code=new_url.short_code,
            created_at=new_url.created_at,
            updated_at=new_url.updated_at,
            created_by=new_url.created_by_id,
            views=new_url.views,
        )

        return response.model_dump(), 201


@url_bp.route("/", methods=["PUT"])
@auth_required
def update_short_url(username):
    try:
        url_data = UpdateUrl.model_validate_json(request.data)
    except:
        raise InvalidInputError

    with Session() as session:
        db_url_data = session.query(Urls).filter_by(id=url_data.id, created_by_id=username).first()
        if not db_url_data:
            raise UrlNotFoundError

        if url_data.url is not None:
            db_url_data.url = url_data.url
        if url_data.short_code is not None:
            db_url_data.short_code = url_data.short_code

        session.commit()
        session.refresh(db_url_data)

        response = CreateUrlResponse(
            id=db_url_data.id,
            url=db_url_data.url,
            short_code=db_url_data.short_code,
            created_at=db_url_data.created_at,
            updated_at=db_url_data.updated_at,
            created_by=db_url_data.created_by_id,
            views=db_url_data.views,
        )

        return response.model_dump(), 201


@url_bp.route("/", methods=["DELETE"])
@auth_required
def delete_short_url(username):
    try:
        url_data = UpdateUrl.model_validate_json(request.data)
    except:
        raise InvalidInputError

    with Session() as session:
        db_url_data = (
            session.query(Urls)
            .filter_by(id=url_data.id, created_by_id=username)
            .first()
        )
        if not db_url_data:
            raise UrlNotFoundError

        session.delete(db_url_data)
        session.commit()

        return "", 202


@url_bp.route("/", methods=["GET"])
@auth_required
def get_short_url(username):
    try:
        url_data = UpdateUrl.model_validate_json(request.data)
    except:
        raise InvalidInputError

    with Session() as session:
        db_url_data = (
            session.query(Urls)
            .filter_by(id=url_data.id, created_by_id=username)
            .first()
        )
        if not db_url_data:
            raise UrlNotFoundError

        response = CreateUrlResponse(
            id=db_url_data.id,
            url=db_url_data.url,
            short_code=db_url_data.short_code,
            created_at=db_url_data.created_at,
            updated_at=db_url_data.updated_at,
            created_by=db_url_data.created_by_id,
            views=db_url_data.views,
        )

        return response.model_dump(), 200
