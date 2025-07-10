import os
import time

import bcrypt
import jwt
from flask import Flask, request

from models import Session, Todo, User
from utils import (
    auth_required,
    validate_login_data,
    validate_register_data,
    validate_todo_data,
)

app = Flask(__name__)
import exceptions

jwt_secret = os.environ.get("JWT_SECRET")
if not jwt_secret:
    raise RuntimeError(
        "JWT_SECRET environment variable is not set. Application cannot start."
    )


@app.route("/register", methods=["POST"])
def register_view():
    data = request.get_json()
    validate_register_data(data=data)

    with Session() as session:
        user_data = session.query(User).filter_by(email=data["email"]).first()

        ### Checks if user alerady exists
        if user_data:
            raise ValueError(f"User {data['email']} already exists")

        ### Encrypt the password
        hash_password = bcrypt.hashpw(
            data["password"].encode("utf-8"), bcrypt.gensalt()
        )

        new_user = User(name=data["name"], email=data["email"], password=hash_password)

        session.add(new_user)
        session.commit()

        return {"message": "User Created succesfully!"}, 201


@app.route("/login", methods=["POST"])
def login_user():
    data = request.get_json()

    validate_login_data(data=data)

    with Session() as session:
        user_data = session.query(User).filter_by(email=data["email"]).first()

        if not user_data or not bcrypt.checkpw(
            data["password"].encode("utf-8"), user_data.password
        ):
            return {"error": "Invalid email or password"}, 401

        jwt_token = jwt.encode(
            {
                "sub": str(user_data.id),
                "exp": int(time.time()) + 3600,
            },
            jwt_secret,
            algorithm="HS256",
        )
        return {
            "message": "User authenticated Successfully",
            "token": jwt_token,
        }, 200


@app.route("/todos", methods=["POST"])
@auth_required
def create_todo(user):
    data = request.get_json()
    validate_todo_data(data)
    new_todo = Todo(title=data["title"], description=data["description"], user_id=user)

    with Session() as session:
        session.add(new_todo)
        session.commit()
        new_todo_json = {
            column.name: getattr(new_todo, column.name)
            for column in Todo.__table__.columns
        }
        return new_todo_json, 201


@app.route("/todos/<int:todo_id>", methods=["PUT"])
@auth_required
def update_todo(user, todo_id):
    data = request.get_json()
    validate_todo_data(data)

    with Session() as session:
        to_do_data = session.query(Todo).filter_by(id=todo_id, user_id=user).first()
        if not to_do_data:
            return {"error": f"Todo with id '{todo_id}' does not exists"}, 404

        to_do_data.title = data["title"]
        to_do_data.description = data["description"]

        session.commit()
        to_do_data_json = {
            column.name: getattr(to_do_data, column.name)
            for column in Todo.__table__.columns
        }
        return to_do_data_json, 200


@app.route("/todos/<int:todo_id>", methods=["DELETE"])
@auth_required
def delete_todo(user, todo_id):
    with Session() as session:
        to_do_data = session.query(Todo).filter_by(id=todo_id, user_id=user).first()
        if not to_do_data:
            return {"error": f"Todo with id '{todo_id}' does not exists"}, 404

    session.delete(to_do_data)
    session.commit()

    return "", 204


@app.route("/todos", methods=["GET"])
@auth_required
def get_todos(user):
    current_page = int(request.args.get("page", 1))
    limit_per_page = int(request.args.get("limit", 10))

    offset = (current_page - 1) * limit_per_page

    with Session() as session:
        todos = (
            session.query(Todo)
            .filter_by(user_id=user)
            .limit(limit_per_page)
            .offset(offset)
            .all()
        )
        todo_list = [
            {
                column.name: getattr(todo, column.name)
                for column in Todo.__table__.columns
            }
            for todo in todos
        ]
        return {"todos": todo_list}, 200
