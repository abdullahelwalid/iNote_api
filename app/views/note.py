from flask import request,jsonify,abort
from datetime import datetime
from app.views import bp
from app import db
from app.models.note import Note
from app.models.user import User



@bp.route('/note', methods=['POST'])
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
    db.session.add(_new_note)
    db.session.commit()

    return jsonify(_new_note.json()), 201

@bp.route('/note', methods=['PUT'])
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
    db.session.commit()
    return jsonify(_note.json()), 201

@bp.route('/note', methods=['DELETE'])
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
    db.session.commit()

    return jsonify("not deleted"), 201

@bp.route('/note')
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
