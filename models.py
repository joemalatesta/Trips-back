import os
from peewee import *
import datetime
from flask_login import UserMixin
from playhouse.db_url import connect


DATABASE = SqliteDatabase('trips.sqlite')


class User(UserMixin, Model):
    username=CharField(unique=True)
    email=CharField(unique=True)
    password=CharField()

    class Meta:
        database = DATABASE


class Trips(Model):
    trip_name = CharField()
    trip_date = CharField()
    about_trip = CharField()
    user = ForeignKeyField(User, backref='trips')

    class Meta:
        database = DATABASE


class Posts(Model):
    user_posts = CharField()
    trip_id = ForeignKeyField(Trips, backref='posts')

    class Meta:
        database = DATABASE


class Pictures(Model):
    trip_pics = CharField()
    post_id = ForeignKeyField(Posts, backref='pictures')

    class Meta:
        database = DATABASE


class Comments(Model):
    comments = CharField()
    pic_id = ForeignKeyField(Pictures, backref='comments')

    class Meta:
        database = DATABASE

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Trips, Posts, Pictures, Comments], safe=True)
    print("TABLES Created")
    DATABASE.close()
