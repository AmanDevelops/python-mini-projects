import base64

from flask import Flask, request

app = Flask(__name__)


def auth_required(f):
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        unauthorized_header = {"WWW-Authenticate": "Basic realm='admin_panel'"}

        if not auth_header:
            return "Username and password Required", 401, unauthorized_header

        try:
            username, password = (
                base64.b64decode(auth_header.split(" ")[1])
                .decode("utf-8")
                .split(":", 1)
            )
        except:
            return "Invalid Credentials format", 401, unauthorized_header

        if username == "admin" and password == "password":
            return f(*args, **kwargs)

        return "Invalid Password", 401, unauthorized_header

    return wrapper


@app.route("/admin")
@auth_required
def home():
    return "Auth Success", 200


@app.route("/logout")
def logout():
    return "Logged out succesfully", 401
