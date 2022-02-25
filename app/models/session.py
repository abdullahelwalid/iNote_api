from app import db
import secrets


class Session(db.Model):
    __tablename__ = "session"
    id = db.Column(
        db.Integer, 
        primary_key=True
        )
    user_id = db.Column(
        db.Integer, 
        db.ForeignKey('user.user_id'), 
        nullable = False
        )
    token = db.Column(
        db.String(256),
        default = secrets.token_urlsafe(16),
        unique = True,
        nullable = False
    )
    user = db.relationship('User')

    def json(self):
        return {
            "token": self.token
        }