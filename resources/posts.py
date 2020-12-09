import models

from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required
from playhouse.shortcuts import model_to_dict


post = Blueprint('posts', 'post')



@post.route('/', methods=["POST"])
@login_required
def create_post():
    try:
        payload = request.get_json()
        created_post = models.Posts.create(
        user_posts=payload['user_posts'],
        trip_id=current_user.id
        )

        post_dict = model_to_dict(created_post)
        return jsonify(data=post_dict, status={"code": 201, "message": "Success"})
    except:
        return jsonify(status={"code": 400, "message": "Not Successful"})


@post.route('/<id>', methods=["GET"])
def get_one_post(id):
    post = models.Post.get_by_id(id)
    return jsonify(data=model_to_dict(post), status={"code": 200, "message": "Success"})


@post.route('/', methods=["GET"])
def get_posts():
    try:
        posts = [model_to_dict(post) for post in models.Posts]
        print(f"here is the list of all my posts. {posts}")
        return jsonify(data=posts, status={"code": 201, "message": "success"})

    except models.DoesNotExist:
        return jsonify(
        data={}, status={"code": 401, "message": "Error getting Resources"})



@post.route('/<id>', methods=["PUT"])
@login_required
def update_post(id):
    payload = request.get_json()
    query = models.Post.update(**payload).where(models.Post.id==id)
    query.execute()
    post = model_to_dict(models.Post.get_by_id(id))
    return jsonify(data=post, status={"code": 200, "message": "Success"})


@post.route('/<id>', methods=["DELETE"])
@login_required
def delete_post(id):
    delete_query = models.Post.delete().where(models.Post.id == id)
    num_of_rows_deleted = delete_query.execute()
    return jsonify(
    data={},
    message="{} So I went home. Didn't post with id {}".format(num_of_rows_deleted, id),
    status={"code": 200}
    )


# end
