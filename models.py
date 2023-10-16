from init import db
from sqlalchemy.ext.declarative import declarative_base
from flask_login import UserMixin
from datetime import datetime

Base = declarative_base()
# userMixin helps flask login function to work.Eg if i use userMixin on User table, User
#  table can use theflask login function
class User(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True, autoincrement=True)
    name = db.Column(db.String(250),nullable=False)
    email = db.Column(db.String(250), primary_key=False,nullable=False,)
    password = db.Column(db.String(250), primary_key=False,nullable=False)
    workouts=db.relationship('Workout',backref='author',lazy=True)


class Workout(db.Model):
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    pushups =db.Column(db.Integer,nullable=False)
    date_posted = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    comment=db.Column(db.Text,nullable=False)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)

