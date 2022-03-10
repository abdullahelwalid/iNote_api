from app import db
from enum import Enum


class User_status(Enum):
    active = 0
    suspended = 1
    terminated = 2
    
class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(
        db.Integer, 
        primary_key = True
        )
    username = db.Column(
        db.String(32), 
        nullable = False
        )
    password = db.Column(
        db.String(64), 
        nullable = False
        )
    email = db.Column(
        db.String(350), 
        nullable = False
        )
    firstname = db.Column(
        db.String(64), 
        nullable = False
        )
    lastname = db.Column(
        db.String(64), 
        nullable = False
        )
    status = db.Column(
        db.Enum(User_status), 
        default = User_status.active, 
        nullable = False
        )

    role = db.relationship("Role", backref = "user")
    user_log = db.relationship("User_log", backref = 'user')

    def json(self):
        return {
            "user id": self.user_id, 
            "username": self.username, 
            "email": self.email,
            "firstname": self.firstname,
            "lastname": self.lastname,
            }