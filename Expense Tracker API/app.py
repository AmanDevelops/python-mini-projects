import os
import time

import bcrypt
import jwt
from flask import Flask, request

from config import jwt_secret
from models import Category, Expense, Session, User
from validators import (
    auth_required,
    validate_create_expense,
    validate_register,
    validate_update_expense,
)

app = Flask(__name__)
import exceptions

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

        return {"message": "User created successfully!"}, 201


@app.route("/auth/login", methods=["POST"])
def login():
    data = request.get_json()
    validate_register(data)

    with Session() as session:
        user_data = session.query(User).filter_by(username=data["username"]).first()

        if not user_data:
            raise ValueError("Either username or password is incorrect")

        if bcrypt.checkpw(data["password"].encode("utf-8"), user_data.password):
            jwt_token = jwt.encode(
                {"sub": str(user_data.id), "exp": int(time.time()) + 3600},
                jwt_secret,
                algorithm="HS256",
            )

            return {
                "message": f"User authenticated successfully",
                "token": jwt_token,
            }, 200

    raise ValueError("Either username or passsword is incorrect")


@app.route("/expenses/create", methods=["POST"])
@auth_required
def create_expense(user):
    data = request.get_json()
    validate_create_expense(data)

    category = data.get("category", "Uncategorized")

    with Session() as session:
        category_data = session.query(Category).filter_by(name=category).first()
        if not category_data:
            category_data = Category(name=category)
            session.add(category_data)
            session.commit()

        new_expense = Expense(
            title=data["title"],
            category_id=category_data.id,
            amount=data["amount"],
            user_id=int(user),
        )
        session.add(new_expense)
        session.commit()

        return {
            "message": "Expense Created!",
            "data": {
                "id": new_expense.id,
                "title": new_expense.title,
                "amount": new_expense.amount,
                "created_at": new_expense.created_at,
                "owner": new_expense.user.username,
            },
        }, 201


@app.route("/expenses/<int:id>", methods=["DELETE"])
@auth_required
def delete_expenses(user, id):
    with Session() as session:
        expenses_data = session.query(Expense).filter_by(id=id, user_id=user).first()
        if not expenses_data:
            raise ValueError(f"Expense with expense_id '{id}' does not exists")

        session.delete(expenses_data)
        session.commit()

        return "", 204


@app.route("/expenses/<int:id>", methods=["PUT"])
@auth_required
def update_expenses(user, id):
    with Session() as session:
        expenses_data = session.query(Expense).filter_by(id=id, user_id=user).first()
        if not expenses_data:
            raise ValueError(f"Expense with expense_id '{id}' does not exists")

        data = request.get_json()
        validate_update_expense(data)

        category_data = session.query(Category).filter_by(name=data["category"]).first()
        if not category_data:
            category_data = Category(name=data["category"])
            session.add(category_data)
            session.commit()

        expenses_data.title = data["title"]
        expenses_data.amount = data["amount"]
        expenses_data.category_id = category_data.id

        session.commit()

        return {
            "message": "Expense Updated",
            "data": {
                "id": expenses_data.id,
                "title": expenses_data.title,
                "amount": expenses_data.amount,
                "created_at": expenses_data.created_at,
                "owner": expenses_data.user.username,
            },
        }, 200


@app.route("/expenses", methods=["GET"])
@auth_required
def get_expenses(user):
    threshold_timestamp = (
        int(time.time()) - int(request.args.get("filter", 365)) * 86400
    )

    with Session() as session:
        expense_data = (
            session.query(Expense)
            .filter(Expense.created_at > threshold_timestamp, Expense.user_id == user)
            .all()
        )

        expense_response = []
        for expense in expense_data:
            expense_response.append(
                {
                    "id": expense.id,
                    "title": expense.title,
                    "amount": expense.amount,
                    "created_at": expense.created_at,
                }
            )
        return {"data": expense_response}, 200
