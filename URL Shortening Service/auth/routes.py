import time

import bcrypt
import jwt
from flask import Blueprint, request

from auth.models import User
from auth.schemas import (
    UserLogin,
    UserLoginResponse,
    UserRegister,
    UserRegisterResponse,
)
from config import JWT_SECRET
from database import Session
from exceptions.custom_exceptions import InvalidInputError, UnauthorizedError

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/register", methods=["POST"])
def register_user():
    try:
        user_data = UserRegister.model_validate_json(request.data)
    except:
        raise InvalidInputError
    with Session() as session:
        is_user_exists = (
            session.query(User).filter_by(username=user_data.username).first()
        )
        if is_user_exists:
            raise InvalidInputError("User Already Exists")

        new_user = User(
            username=user_data.username,
            password=bcrypt.hashpw(
                user_data.password.encode(), bcrypt.gensalt()
            ).decode(),
        )

        session.add(new_user)
        session.commit()

    response = UserRegisterResponse()

    return response.model_dump(), 201


@auth_bp.route("/login", methods=["POST"])
def login_user():
    try:
        user_data = UserLogin.model_validate_json(request.data)
    except:
        raise InvalidInputError
    with Session() as session:
        db_user_data = (
            session.query(User).filter_by(username=user_data.username).first()
        )

        if not db_user_data:
            raise InvalidInputError("User Does Not Exists", 404)

        if bcrypt.checkpw(user_data.password.encode(), db_user_data.password.encode()):
            current_time = time.time() // 1
            payload = {
                "sub": str(db_user_data.id),
                "exp": current_time + 3600,
                "iat": current_time,
            }
            jwt_token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")
            response = UserLoginResponse(token=jwt_token)
            return response.model_dump(), 200

        raise UnauthorizedError
