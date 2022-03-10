from flask import jsonify, abort, request
import hashlib
from flask_jwt_extended import create_access_token
import datetime
from app.views import bp
from app.models.user import User
from app.models.role import Role, Roles_enum
from app.models.user_log import User_log
from app import db

@bp.route('/signup', methods=['POST'])
def signup():
    if not request.json:
        abort(400, "response should be a JSON object")
    _data = request.json
    def _validate(request) -> bool:
        if "username" not in request:
            return False
        if "password" not in request:
            return False
        if "email" not in request:
            return False
        if "firstname" not in request:
            return False 
        if "lastname" not in request:
            return False
        return True
    if not _validate(_data):
        abort(400, "One or more fields required")
    
    _username = _data['username']
    _password = hashlib.sha256(_data['password'].encode()).hexdigest()
    _email = _data['email']
    _firstname = _data['firstname']
    _lastname = _data['lastname']

    if User.query.filter_by(email=_email).first():
        abort(400, "Email is already registered")
    if User.query.filter_by(username=_username).first():
        abort(400, "Username already exist")

    user = User(
        username = _username,
        password = _password,
        firstname = _firstname,
        lastname = _lastname,
        email = _email
    )
    role = Role(user_id = user.user_id, role = Roles_enum.user)
    user_log = User_log(user_id = user.user_id, user_activity = "Account created")
    user.role.append(role)
    user.user_log.append(user_log)
    db.session.add(user)
    db.session.commit()
    return jsonify(user.json()), 201


@bp.route('/login', methods=['post'])
def login():
    if not request.json:
        abort(400, "response should be a JSON object")
    _data = request.json
    def _validate(request) -> bool:
        if 'username' not in request and 'email' not in request:
            return False
        if 'password' not in request:
            return False
        return True
    if not _validate(_data):
        abort(400, "one or more field is required")

    _password = hashlib.sha256(_data['password'].encode()).hexdigest()
    def _validate_user(password) -> bool:
        if 'username' in _data:
            user = User.query.filter(
                db.func.lower(User.username) == _data['username'].lower()
                    ).first()
            if not user:
                return False
            if user.password == password:
                user_log = User_log(user_id = user.user_id, user_activity = "user logged in")
                user.user_log.append(user_log)
                db.session.commit()
                return True
            return False
        if 'email' in _data:
            user = User.query.filter(
                db.func.lower(User.email) == _data['email'].lower()
            ).first()

            if not user:
                return False
            if user.password == password:
                user_log = User_log(user_id = user.user_id, user_activity = "user logged in")
                user.user_log.append(user_log)
                db.session.commit()
                return True
            return False
    
    if not _validate_user(_password):
        abort(404, "user not found")

    if "username" in _data:
        _user = User.query.filter(
            db.func.lower(User.username) == _data['username'].lower()
            ).first()
    else:
        _user = User.query.filter(
            db.func.lower(User.email) == _data['email'].lower()
            ).first()
    expires = datetime.timedelta(days=1)
    access_token = create_access_token(identity=str(_user.user_id), expires_delta=expires)
    return jsonify({
        "token": access_token
    }), 201
