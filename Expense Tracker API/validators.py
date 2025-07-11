
import jwt
from flask import request

from config import jwt_secret


def validate_register(data):
    required_fields = ("username", "password")

    missing_fields = [field for field in required_fields if not data.get(field)]

    if missing_fields:
        raise ValueError(f"Missing required field(s): {', '.join(missing_fields)}")

    not_string = [
        field for field in required_fields if not isinstance(data[field], str)
    ]

    if not_string:
        raise ValueError(f"{', '.join(not_string)} field(s) must be string.")

    if len(data["password"]) < 8:
        raise ValueError("Password must be at least 8 characters long.")


def auth_required(f):
    def wrapper(*args, **kwargs):
        try:
            jwt_token = request.headers.get("Authorization").split(" ")[1]
        except Exception:
            raise ValueError("Please Provide a JWT Token")

        try:
            user = jwt.decode(jwt_token, jwt_secret, algorithms=["HS256"])["sub"]
        except jwt.InvalidTokenError:
            raise ValueError("Invalid or expired JWT Token")

        return f(user=user, *args, **kwargs)

    return wrapper
