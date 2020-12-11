import models


from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required
from playhouse.shortcuts import model_to_dict


trip = Blueprint('trips', 'trip')


@trip.route('/', methods=["POST"])
@login_required
def create_trip():
    try:
        payload = request.get_json()
        created_trip = models.Trips.create(
        trip_name = payload['trip_name'],
        trip_date = payload['trip_date'],
        about_trip = payload['about_trip'],
        user_posts = payload['user_posts'],
        trip_pics = payload['trip_pics'],
        user = current_user.id
        )
        trip_dict = model_to_dict(created_trip)
        return jsonify(data=trip_dict, status={"code": 201, "message": "Success"})
    except:
        return jsonify(status={"code": 400, "message": "Not Successful creating the trip"})


@trip.route('/all', methods=['GET'])
def get_all_the_trips():
    try:
        all_trips = [model_to_dict(trip) for trip in models.Trips]
        print(f"here is the list of the Users trips. {all_trips}")
        return jsonify(data=all_trips, status={"code": 201, "message": "success"})

    except models.DoesNotExist:
        return jsonify(
        data={}, status={"code": 401, "message": "Error getting Resources"})


@trip.route('/', methods=['GET'])
@login_required
def get_all_my_trips():
    try:
        trips = [model_to_dict(trip) for trip in current_user.trips]
        print(f"here is the list of all my trips. {trips}")
        return jsonify(data=trips, status={"code": 201, "message": "success"})

    except models.DoesNotExist:
        return jsonify(
        data={}, status={"code": 401, "message": "Error getting Resources"})


@trip.route('/<id>', methods=["GET"])
def get_one_trip(id):
    trip = models.Trips.get_by_id(id)
    return jsonify(data=model_to_dict(trip), status={"code": 200, "message": "Success"})


@trip.route('/<id>', methods=["PUT"])
def update_trip(id):
    payload = request.get_json()
    query = models.Trips.update(**payload).where(models.Trips.id==id)
    query.execute()
    trip = model_to_dict(models.Trips.get_by_id(id))
    return jsonify(data=trip, status={"code": 200, "message": "Success"})


@trip.route('/<id>', methods=["DELETE"])
def delete_trip(id):
    delete_query = models.Trips.delete().where(models.Trips.id == id)
    num_of_rows_deleted = delete_query.execute()
    return jsonify(
    data={},
    message="{} So I went home. Didn't go on trip with id {}".format(num_of_rows_deleted, id),
    status={"code": 200}
    )

@trip.route('/posts/', methods=["GET"])
def get_posts():
    try:
        posts = [model_to_dict(post) for post in models.Posts]
        return jsonify(data=posts, status={"code": 201, "message": "success"})

    except models.DoesNotExist:
        return jsonify(
        data={}, status={"code": 401, "message": "Error getting Resources"})


@trip.route('/posts/', methods=["POST"])
@login_required
def create_post():
    try:

        payload = request.get_json()
        created_post = models.Posts.create(
        user_posts = payload['user_posts'],
        trip_id = current_user.id
        )
        post_dict = model_to_dict(created_post)
        return jsonify(data=post_dict, status={"code": 201, "message": "Success"})
    except:
        return jsonify(status={"code": 400, "message": "Not Successful"})


@trip.route('/posts/<id>', methods=["GET"])
def get_one_post(id):
    post = models.Post.get_by_id(id)
    return jsonify(data=model_to_dict(post), status={"code": 200, "message": "Success"})


@trip.route('/posts/<id>', methods=["PUT"])
@login_required
def update_post(id):
    payload = request.get_json()
    query = models.Post.update(**payload).where(models.Post.id==id)
    query.execute()
    post = model_to_dict(models.Post.get_by_id(id))
    return jsonify(data=post, status={"code": 200, "message": "Success"})


@trip.route('/posts/<id>', methods=["DELETE"])
@login_required
def delete_post(id):
    delete_query = models.Post.delete().where(models.Post.id == id)
    num_of_rows_deleted = delete_query.execute()
    return jsonify(
    data={},
    message="{} So I went home. Didn't post with id {}".format(num_of_rows_deleted, id),
    status={"code": 200}
    )



@trip.route('/pics/', methods=['GET'])
def get_all_my_pictures():
    try:
        pictures = [model_to_dict(picture) for picture in models.Pictures]
        return jsonify(data=pictures, status={"code": 201, "message": "success"})

    except models.DoesNotExist:
        return jsonify(
        data={}, status={"code": 401, "message": "Error getting Resources"})


@trip.route('/pics/', methods=["POST"])
def create_picture():
    try:
        payload = request.get_json()
        created_picture = models.Pictures.create(
        trip_pics=payload['trip_pics'],
        post=current_user.id
        )

        picture_dict = model_to_dict(created_picture)
        to_return = jsonify(data=picture_dict, status={"code": 201, "message": "Success"})
        return to_return
    except:
        return jsonify(status={"code": 400, "message": "Not Successful"})


@trip.route('/pics/<id>', methods=["GET"])
def get_one_picture(id):
    picture = models.Picture.get_by_id(id)
    return jsonify(data=model_to_dict(picture), status={"code": 200, "message": "Success"})


@trip.route('/pics/<id>', methods=["PUT"])
def update_picture(id):
    payload = request.get_json()
    query = models.Picture.update(**payload).where(models.Picture.id==id)
    query.execute()
    picture = model_to_dict(models.Picture.get_by_id(id))
    return jsonify(data=picture, status={"code": 200, "message": "Success"})


@trip.route('/pics/<id>', methods=["DELETE"])
def delete_picture(id):
    delete_query = models.Picture.delete().where(models.Picture.id == id)
    num_of_rows_deleted = delete_query.execute()
    return jsonify(
    data={},
    message="{} So I went home. Didn't go on picture with id {}".format(num_of_rows_deleted, id),
    status={"code": 200}
    )





# end
