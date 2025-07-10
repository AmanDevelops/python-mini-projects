from flask import Flask, request
from flask.views import MethodView

from models import Category, Post, Session

app = Flask(__name__)


@app.route("/posts", methods=["POST"])
def create_post():
    data = request.get_json()

    # Validates Data
    missing_fields = [
        field for field in ("title", "content", "category") if not data.get(field)
    ]
    if missing_fields:
        return {
            "success": False,
            "message": f"Missing required fields: {', '.join(missing_fields)}",
        }, 400

    tag_data_type = type(data.get("tags"))
    if tag_data_type is not list:
        return {
            "success": False,
            "message": f"Tags must me in list format not {tag_data_type.__name__}",
        }, 400

    with Session() as session:
        category_name = data["category"].lower()
        category = session.query(Category).filter_by(name=category_name).first()
        if category is None:
            category = Category(name=category_name)
            session.add(category)
            session.commit()

        new_post = Post(
            title=data["title"],
            content=data["content"],
            category=category.id,
            tags=data.get("tags", []),
        )
        session.add(new_post)
        session.commit()

        # Prepare Response
        post_data = {
            column.name: getattr(new_post, column.name)
            for column in Post.__table__.columns
        }
        post_data["category"] = data.get("category")

        return {
            "success": True,
            "message": "Post created successfully",
            "data": post_data,
        }, 201


@app.route("/posts", methods=["GET"])
def get_post():
    with Session() as session:
        posts_data = session.query(Post).all()

        posts = [
            {
                **{
                    column.name: getattr(post, column.name)
                    for column in Post.__table__.columns
                },
                "category": post.category_relationship.name if post.category_relationship else None,
            }
            for post in posts_data
        ]
        return posts
