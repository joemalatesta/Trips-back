import models


from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required
from playhouse.shortcuts import model_to_dict


trip = Blueprint('trips', 'trip')


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


@trip.route('/', methods=["POST"])
@login_required
def create_trip():
    # try:
    payload = request.get_json()
    created_trip = models.Trips.create(
    trip_name=payload['trip_name'],
    trip_date=payload['trip_date'],
    about_trip=payload['about_trip'],
    user=current_user.id
    )
    trip_dict = model_to_dict(created_trip)
    return jsonify(data=trip_dict, status={"code": 201, "message": "Success"})
    # except:
    #     return jsonify(status={"code": 400, "message": "Not Successful creating the trip"})


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


# end
