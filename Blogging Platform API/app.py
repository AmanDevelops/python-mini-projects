from flask import Flask, request
from sqlalchemy import or_

from models import Category, Post, Session

app = Flask(__name__)


@app.route("/posts", methods=["GET"])
def get_post():
    is_query = request.args.get("term")

    with Session() as session:

        if is_query is not None:
            posts_data = (
                session.query(Post)
                .join(Post.category_relationship)
                .filter(
                    or_(
                        Post.title.ilike(f"%{is_query}%"),
                        Post.content.ilike(f"%{is_query}%"),
                        Category.name.ilike(f"%{is_query}%"),
                    )
                )
                .all()
            )

        else:
            posts_data = session.query(Post).all()

        posts = [
            {
                **{
                    column.name: getattr(post, column.name)
                    for column in Post.__table__.columns
                },
                "category": (
                    post.category_relationship.name
                    if post.category_relationship
                    else None
                ),
            }
            for post in posts_data
        ]

        posts = {"success": True, "data": posts}
        return posts, 200


@app.route("/posts/<int:post_id>", methods=["GET"])
def get_single_post(post_id):
    with Session() as session:
        post_data_response = session.query(Post).filter_by(id=post_id).first()
        if post_data_response is None:
            return {
                "success": False,
                "message": f"Post with post id: {post_id} does not exists",
            }, 404
        post_data = {
            **{
                column.name: getattr(post_data_response, column.name)
                for column in Post.__table__.columns
            },
            "category": post_data_response.category_relationship.name,
        }
        post_data = {"success": True, "data": post_data}
        return post_data, 200


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


@app.route("/posts/<int:post_id>", methods=["PUT"])
def update_single_post(post_id):
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
        post_data_response = session.query(Post).filter_by(id=post_id).first()
        if post_data_response is None:
            return {
                "success": False,
                "message": f"Post with post id: {post_id} does not exists",
            }, 404

        category_name = data["category"].lower()
        category = session.query(Category).filter_by(name=category_name).first()
        if category is None:
            category = Category(name=category_name)
            session.add(category)
            session.commit()

        post_data_response.title = data["title"]
        post_data_response.content = data["content"]
        post_data_response.category = category.id
        post_data_response.tags = data["tags"]
        session.commit()

        post_data = {
            **{
                column.name: getattr(post_data_response, column.name)
                for column in Post.__table__.columns
            },
            "category": post_data_response.category_relationship.name,
        }

        return {
            "success": True,
            "message": "Post updated successfully",
            "data": post_data,
        }, 200


@app.route("/posts/<int:post_id>", methods=["DELETE"])
def delete_single_post(post_id):
    with Session() as session:
        post_data_response = session.query(Post).filter_by(id=post_id).first()
        if post_data_response is None:
            return {
                "success": False,
                "message": f"Post with post id: {post_id} does not exists",
            }, 404
        session.delete(post_data_response)
        session.commit()
        return "", 204
