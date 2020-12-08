import models


from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required
from playhouse.shortcuts import model_to_dict


comment = Blueprint('comments', 'comment')



@comment.route('/', methods=['GET'])
def get_all_my_comments():
    try:
        comments = [model_to_dict(comment) for comment in models.Comments]
        print(f"here is the list of comments. {comments}")
        return jsonify(data=comments, status={"code": 201, "message": "success"})

    except models.DoesNotExist:
        return jsonify(
        data={}, status={"code": 401, "message": "Error getting Resources"})


@comment.route('/', methods=["POST"])

def create_comment():
    try:
        payload = request.get_json()
        print(payload)
        created_comment = models.Comments.create(
        comments=payload['comments'],
        pic_id=current_user.id
        )

        comment_dict = model_to_dict(created_comment)
        to_return = jsonify(data=comment_dict, status={"code": 201, "message": "Success"})
        print(to_return)
        return to_return
    except:
        return jsonify(status={"code": 400, "message": "Not Successful"})


@comment.route('/<id>', methods=["GET"])
def get_one_comment(id):
    comment = models.Comment.get_by_id(id)
    return jsonify(data=model_to_dict(comment), status={"code": 200, "message": "Success"})


@comment.route('/<id>', methods=["PUT"])
def update_comment(id):
    payload = request.get_json()
    query = models.Comment.update(**payload).where(models.Comment.id==id)
    query.execute()
    comment = model_to_dict(models.Comment.get_by_id(id))
    return jsonify(data=comment, status={"code": 200, "message": "Success"})


@comment.route('/<id>', methods=["DELETE"])
def delete_comment(id):
    delete_query = models.Comment.delete().where(models.Comment.id == id)
    num_of_rows_deleted = delete_query.execute()
    return jsonify(
    data={},
    message="{} So I went home. Didn't go on comment with id {}".format(num_of_rows_deleted, id),
    status={"code": 200}
    )


# end
