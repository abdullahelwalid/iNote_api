from app import db
from enum import Enum

class Roles_enum(Enum):
    user = 464
    admin = 454
    superadmin = 474

class Role(db.Model):
    __tablename__ = "role"
    id = db.Column(
        db.Integer,
        primary_key = True
    )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.user_id'),
        unique = True,
        nullable = False
    )
    role = db.Column(
        db.Enum(Roles_enum),
        nullable = False,
        default = Roles_enum.user
    )

    def json(self):
        return {
            "user id": self.user_id,
            "role": self.role
        }