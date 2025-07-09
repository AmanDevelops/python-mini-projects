import base64
from datetime import datetime

from db import Database
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
database = Database()


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

    wrapper.__name__ = f.__name__
    return wrapper


@app.route("/")
def home():
    posts = [
        post
        for post in database.posts
        if datetime.strptime(post["date"], "%Y-%m-%dT%H:%M") < datetime.now()
    ]

    print(posts)

    return render_template("index.html", posts=posts)


@app.route("/article/<int:id>")
def view_post(id):
    try:
        post_data = database.get_post(id)
        if post_data is None:
            raise IndexError
    except IndexError:
        return "Post Not found", 404
    return render_template("view_post.html", post=post_data)


@app.route("/admin")
@auth_required
def view_admin_dashboard():
    return render_template("admin_dashboard.html", posts=database.posts)


@app.route("/admin/new", methods=["GET", "POST"])
@auth_required
def new_post_view():
    if request.method == "POST":
        database.add_post(
            title=request.form.get("title"),
            date=request.form.get("pub_date"),
            content=request.form.get("content"),
        )
        return redirect(url_for("view_admin_dashboard"))
    return render_template("new_post.html")


@app.route("/admin/edit/<int:id>", methods=["GET", "POST"])
@auth_required
def edit_posts(id):
    try:
        post_data = database.get_post(id)
        if post_data is None:
            raise IndexError
        if request.method == "POST":
            database.update_post(
                id=id,
                title=request.form.get("title"),
                date=request.form.get("pub_date"),
                content=request.form.get("content"),
            )
        post_data = database.get_post(id)

        return render_template("edit_post.html", post=post_data)
    except:
        return "Post Not found", 404


@app.route("/admin/delete/<int:id>")
@auth_required
def view_delete_post(id):
    database.delete_post(id)
    return redirect(url_for("view_admin_dashboard"))


@app.route("/logout")
def logout():
    return "Logged out succesfully", 401
