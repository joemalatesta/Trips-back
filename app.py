from flask import Flask, jsonify, g
from flask_cors import CORS
from flask_mail import Mail, Message
from resources.users import user
from resources.trips import trip
from resources.comments import comment
from flask_login import LoginManager, current_user, login_required
from playhouse.shortcuts import model_to_dict
from peewee import *


import os
import models
import datetime

DEBUG = True
PORT = 8000

app = Flask(__name__)

app.secret_key = "Dust Bunnies Snuggle best with Dirty Dogs"
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'thatguyfromcodingcamp@gmail.com'
app.config['MAIL_PASSWORD'] = 'campcamp'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True


if 'ON_HEROKU' in os.environ:
    app.config.update(
        SESSION_COOKIE_SECURE=True,
        SESSION_COOKIE_SAMESITE='None'
    )

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    try:
        user = models.User.get_by_id(user_id)
        return user
    except models.DoesNotExist:
        return None


CORS(user, origins=['http://localhost:3000', 'https://tripsfrontend-app.herokuapp.com'], supports_credentials=True)
CORS(trip, origins=['http://localhost:3000', 'https://tripsfrontend-app.herokuapp.com'], supports_credentials=True)
CORS(comment, origins=['http://localhost:3000', 'https://tripsfrontend-app.herokuapp.com'], supports_credentials=True)


app.register_blueprint(user, url_prefix='/api/users')
app.register_blueprint(trip, url_prefix='/api/trips')
app.register_blueprint(comment, url_prefix='/api/comments')

mail = Mail(app)

@app.route("/send/<id>")
def index():
    msg = Message("I got to my favorite spot!!",  sender = "thatguyfromcodingcamp@gmail.com",
        recipients=[{trips.user.email}])
    msg.body = "everything is going well!!"
    mail.send(msg)
    return jsonify(data={}, status={"code": 201, "message": "success"})


@app.route('/')
def index():
    return 'This is Trips'


@app.before_request
def before_request():
    g.db = models.DATABASE
    g.db.connect()


@app.after_request
def after_request(response):
    g.db.close()
    return response


if 'ON_HEROKU' in os.environ:
    print('\non heroku!')
    models.initialize()

if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT)


# end
