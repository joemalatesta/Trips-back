import os
from peewee import *
import datetime
from flask_login import UserMixin
from playhouse.db_url import connect


if 'ON_HEROKU' in os.environ:
    DATABASE = connect(os.environ.get('DATABASE_URL'))
else:
    DATABASE = SqliteDatabase('trips.sqlite')


class User(UserMixin, Model):
    username=TextField(unique=True)
    email=TextField(unique=True)
    password=CharField()

    class Meta:
        database = DATABASE


class Trips(Model):
    trip_name=TextField()
    trip_date=CharField()
    user_posts=CharField()
    trip_pics=CharField()
    user=ForeignKeyField(User, backref='trips')
    class Meta:
        database = DATABASE


class Comments(Model):
    comments = CharField()
    pic_id = ForeignKeyField(Trips, backref='comments')

    class Meta:
        database = DATABASE


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Trips, Comments], safe=True)
    print("TABLES Created")
    DATABASE.close()
