import models


from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required
from playhouse.shortcuts import model_to_dict


picture = Blueprint('pictures', 'picture')



@picture.route('/', methods=['GET'])
def get_all_my_pictures():
    try:
        pictures = [model_to_dict(picture) for picture in models.Pictures]
        print(f"here is the list of pictures. {pictures}")
        return jsonify(data=pictures, status={"code": 201, "message": "success"})

    except models.DoesNotExist:
        return jsonify(
        data={}, status={"code": 401, "message": "Error getting Resources"})


@picture.route('/', methods=["POST"])

def create_picture():
    try:
        payload = request.get_json()
        print(payload)
        created_picture = models.Pictures.create(
        trip_pics=payload['trip_pics'],
        post_id=current_user.id
        )

        picture_dict = model_to_dict(created_picture)
        to_return = jsonify(data=picture_dict, status={"code": 201, "message": "Success"})
        print(to_return)
        return to_return
    except:
        return jsonify(status={"code": 400, "message": "Not Successful"})


@picture.route('/<id>', methods=["GET"])
def get_one_picture(id):
    picture = models.Picture.get_by_id(id)
    return jsonify(data=model_to_dict(picture), status={"code": 200, "message": "Success"})


@picture.route('/<id>', methods=["PUT"])
def update_picture(id):
    payload = request.get_json()
    query = models.Picture.update(**payload).where(models.Picture.id==id)
    query.execute()
    picture = model_to_dict(models.Picture.get_by_id(id))
    return jsonify(data=picture, status={"code": 200, "message": "Success"})


@picture.route('/<id>', methods=["DELETE"])
def delete_picture(id):
    delete_query = models.Picture.delete().where(models.Picture.id == id)
    num_of_rows_deleted = delete_query.execute()
    return jsonify(
    data={},
    message="{} So I went home. Didn't go on picture with id {}".format(num_of_rows_deleted, id),
    status={"code": 200}
    )


# end
