import os
import re

import jwt
from flask import request

jwt_secret = os.environ.get("JWT_SECRET")


# ============== Validate user input ===============


def validate_register_data(data):
    # Checks if Data is dict
    if not isinstance(data, dict):
        raise ValueError("Invalid input: expected a JSON object (dictionary)")

    # Checks if email and password exists
    required_fields = ("email", "password", "name")
    missing_fields = [field for field in required_fields if not data.get(field)]
    if missing_fields:
        raise ValueError(f"Missing required field(s): {', '.join(missing_fields)}")

    # Checks if email and password are string
    if not isinstance(data["email"], str) or not isinstance(data["password"], str):
        raise ValueError("Email and password must be strings")

    # Checks if email is a valid email
    email_pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    if not re.match(email_pattern, data["email"]):
        raise ValueError(f"Email '{data['email']}' is not a valid email")


def validate_login_data(data):
    # Checks if Data is dict
    if not isinstance(data, dict):
        raise ValueError("Invalid input: expected a JSON object (dictionary)")

    # Checks if email and password exists
    required_fields = ("email", "password")
    missing_fields = [field for field in required_fields if not data.get(field)]
    if missing_fields:
        raise ValueError(f"Missing required field(s): {', '.join(missing_fields)}")

    # Checks if email and password are string
    if not isinstance(data["email"], str) or not isinstance(data["password"], str):
        raise ValueError("Email and password must be strings")

    # Checks if email is a valid email
    email_pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    if not re.match(email_pattern, data["email"]):
        raise ValueError(f"Email '{data['email']}' is not a valid email")


def validate_todo_data(data):
    if not isinstance(data, dict):
        raise ValueError("Invalid input: expected a JSON object (dictionary)")

    required_fields = ("title", "description")
    missing_fields = [field for field in required_fields if not data.get(field)]
    if missing_fields:
        raise ValueError(f"Missing required field(s): {', '.join(missing_fields)}")

    if not isinstance(data["title"], str) or not isinstance(data["description"], str):
        raise ValueError("Title and Description must be strings")


# ====================== Decorators ==================


def auth_required(f):
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        # print(auth_header)
        if auth_header is not None:
            jwt_token = auth_header.split(" ")[1]
            if jwt_token is not None:
                try:
                    content = jwt.decode(jwt_token, jwt_secret, algorithms=["HS256"])
                except:
                    return {"error": "Unauthorized"}, 401
                return f(user=content["sub"], *args, **kwargs)
        return {"error": "Unauthorized"}, 401

    wrapper.__name__ = f.__name__
    return wrapper
