from datetime import datetime
from app import db


class User_log(db.Model):
    __tablename__ = "user_log"
    id = db.Column(
        db.Integer, 
        primary_key=True
        )
    user_id = db.Column(
        db.Integer, 
        db.ForeignKey('user.user_id'),
        nullable = False
        )
    user_activity = db.Column(
        db.String(256),
        nullable = False
    ),
    date_time = db.Column(
        db.DateTime,
        default = datetime.now()
    )
    
    def json(self):
        return {
            "user id": self.user_id,
            "user activity": self.user_activity
        }