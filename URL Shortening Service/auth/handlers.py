import jwt
from flask import request

from config import JWT_SECRET
from exceptions.custom_exceptions import InvalidInputError, InvalidJWTError


def auth_required(f):
    def wrapper(*args, **kwargs):
        try:
            jwt_token = request.headers.get("Authorization").split(" ")[1]
        except Exception:
            raise InvalidInputError("Invalid Authorization Code")

        try:
            username = jwt.decode(jwt_token, JWT_SECRET, algorithms=["HS256"])["sub"]
        except jwt.InvalidTokenError:
            raise InvalidJWTError

        return f(username=username, *args, **kwargs)

    wrapper.__name__ = f.__name__
    return wrapper
