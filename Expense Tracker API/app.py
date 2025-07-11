import os
import time

import bcrypt
import jwt
from flask import Flask, request

from models import Category, Expense, Session, User
from validators import validate_register

app = Flask(__name__)
import exceptions

jwt_secret = os.environ.get("JWT_SECRET")
if jwt_secret is None:
    raise RuntimeError("Please setup the JWT secret key to the environment variables.")


@app.route("/")
def home():
    return "<h1>Welcome to Expense Tracker API</h1>"


@app.route("/auth/register", methods=["POST"])
def register():
    data = request.get_json()
    validate_register(data)

    with Session() as session:
        user_data = session.query(User).filter_by(username=data["username"]).first()

        if user_data:
            raise ValueError(f"Username '{data['username']}' already exists")

        new_user = User(
            username=data["username"],
            password=bcrypt.hashpw(data["password"].encode("utf-8"), bcrypt.gensalt()),
        )

        session.add(new_user)
        session.commit()

        return {"message": "User created succesfully!"}, 201


@app.route("/auth/login", methods=["POST"])
def login():
    data = request.get_json()
    validate_register(data)

    with Session() as session:
        user_data = session.query(User).filter_by(username=data["username"]).first()

        if not user_data:
            raise ValueError("Either username or passsword is incorrect")


        if bcrypt.checkpw(data["password"].encode("utf-8"), user_data.password):
            jwt_token = jwt.encode(
                {"sub": user_data.id, "exp": int(time.time()) + 3600},
                os.environ.get("JWT_SECRET"),
                algorithm="HS256",
            )

            return {"message": "User authnticated succesfully", "token": jwt_token}, 200
        
    raise ValueError("Either username or passsword is incorrect")
