from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

# in python the class name needs to be capital
# databases stores table name as lowercase letters
# this is the reason why we write 'user.id' instead of
# User.id
# we need to write Capital when declaring relationship
# it is what it is

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class  User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')