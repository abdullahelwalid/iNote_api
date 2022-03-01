from app import db
from datetime import datetime

class Note(db.Model):
    __tablename__ = "note"
    note_id = db.Column(
        db.Integer,
        primary_key = True
        )
    note = db.Column(
        db.String(1000),
        nullable=False
        )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.user_id'),
        nullable=False
    )
    date_added = db.Column(
        db.DateTime,
        nullable = True,
        default = datetime.now()
    )
    date_modified = db.Column(
        db.DateTime,
        nullable = True
    )

    reminder = db.Column(
        db.DateTime,
        nullable = True
    )

    db.relationship('User', backref = 'note', lazy='dynamic')

    def json(self):
        return {
            "note id": self.note_id,
            "note": self.note,
            "user id": self.user_id,
            "date added": self.date_added,
            "date modified": self.date_modified,
            "reminder": self.reminder
        }