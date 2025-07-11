import bcrypt
from flask import Flask, request

from models import Category, Expense, Session, User
from validators import validate_register

app = Flask(__name__)
import exceptions


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
            raise ValueError(f"Username {data['username']} already exists")

        new_user = User(
            username=data["username"],
            password=bcrypt.hashpw(data["password"].encode("utf-8"), bcrypt.gensalt()),
        )

        session.add(new_user)
        session.commit()

        return {"message": "User created succesfully!"}, 201
