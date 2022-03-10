from flask import request,jsonify,abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from app.views import bp
from app import db
from app.models.note import Note
from app.models.user import User
from app.models.user_log import User_log


@bp.route('/note', methods=['POST'])
@jwt_required()
def add_note():
    if not request.json:
        abort(400, "Data is not JSON")
    _data = request.json
    def _validate(request) -> bool:
        if "user_id" not in request:
            return False
        if "note" not in request:
            return False
        return True

    if not _validate(_data):
        abort(400, "one or more data field is required")

    _note = _data['note']
    _user_id = _data['user_id']
    _user = User.query.filter_by(user_id = _user_id).first()
    if not _user:
        abort(404, "user doesn't exist")

    _new_note = Note(
        note = _note,
        user_id = _user_id
    )
    user_log = User_log(user_id = _user.user_id, user_activity = "user created a note")
    _user.user_log.append(user_log)
    db.session.add(_new_note)
    db.session.commit()

    return jsonify(_new_note.json()), 201

@bp.route('/note', methods=['PUT'])
@jwt_required()
def edit_note():
    if not request.json:
        abort(400, "Response should be in JSON")
    _data = request.json
    def _validate(request) -> bool:
        if "note_id" not in request:
            return False
        if "user_id" not in request:
            return False
        if "new_note" not in request:
            return False
        return True
    if not _validate(_data):
        abort(400, "one or more data field is missing")
    _user_id = _data['user_id']
    _note_id = _data['note_id']
    _new_note = _data['new_note']

    _user = User.query.filter_by(user_id = _user_id).first()
    _note = Note.query.filter_by(note_id = _note_id).first()

    if not _user or not _note:
        abort(404, "note or user doesn't exist")
    
    _note.note = _new_note
    _note.date_modified = datetime.now()
    user_log = User_log(user_id = _user.user_id, user_activity = f"user modified a note with the id {_note.note_id}")
    _user.user_log.append(user_log)
    db.session.commit()
    return jsonify({
        "note": _note.json(),
        "user": get_jwt_identity()
        }), 201

@bp.route('/note', methods=['DELETE'])
@jwt_required()
def delete_note():
    if not request.json:
        abort(400, "Response should be in JSON")
    _data = request.json
    def _validate(request) -> bool:
        if "note_id" not in request:
            return False
        if "user_id" not in request:
            return False
        return True
    if not _validate(_data):
        abort(400, "one or more data field is missing")

    _user_id = _data['user_id']
    _note_id = _data['note_id']

    _user = User.query.filter_by(user_id = _user_id).first()
    _note = Note.query.filter_by(note_id = _note_id).first()

    if not _user or not _note:
        abort(404, "note or user doesn't exist")
    
    db.session.delete(_note)
    _user_log = User_log(user_id = _user.user_id, user_activity = f"note with the id {_note.note_id} has been deleted")
    db.session.commit()

    return jsonify("not deleted"), 201

@bp.route('/note')
@jwt_required()
def get_user_notes():
    if not request.json:
        abort(400, "Response should be in JSON")
    _data = request.json
    def _validate(request) -> bool:
        if "user_id" not in request:
            return False
        return True
    if not _validate(_data):
        abort(400, "one or more data field is required")
    _user_id = _data['user_id']
    _user = User.query.filter_by(user_id = _user_id).first()
    if not _user:
        abort(404, "user doesn't exist")

    _notes = Note.query.filter_by(user_id = _user_id).all()
    return jsonify({
        "notes": [note.json() for note in _notes]
        })