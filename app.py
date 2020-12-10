from flask import Flask, jsonify, g
from flask_cors import CORS
from flask_mail import Mail, Message
from resources.users import user
from resources.trips import trip
from resources.comments import comment
from resources.posts import post
from resources.pictures import picture
from flask_login import LoginManager, current_user, login_required
from playhouse.shortcuts import model_to_dict
from peewee import *


import os
import models
import datetime


DEBUG = True
PORT = 8000


app = Flask(__name__)
mail = Mail(app)

app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_SAMESITE='None'
)

app.secret_key = "Dust Bunnies Snuggle best with Dirty Dogs"

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    try:
        user = models.User.get_by_id(user_id)
        return user
    except models.DoesNotExist:
        return None


CORS(user, origins=['http://localhost:3000'], supports_credentials=True)
CORS(trip, origins=['http://localhost:3000'], supports_credentials=True)
CORS(post, origins=['http://localhost:3000'], supports_credentials=True)
CORS(picture, origins=['http://localhost:3000'], supports_credentials=True)
CORS(comment, origins=['http://localhost:3000'], supports_credentials=True)


app.register_blueprint(user, url_prefix='/api/users')
app.register_blueprint(trip, url_prefix='/api/trips')
app.register_blueprint(post, url_prefix='/api/posts')
app.register_blueprint(picture, url_prefix='/api/pictures')
app.register_blueprint(comment, url_prefix='/api/comments')


@app.route('/')
def index():
	return 'This is Trips and Adventures'


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
