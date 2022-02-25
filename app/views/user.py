from flask import jsonify, abort, request
import hashlib
from app.views import bp
from app.models.user import User
from app.models.role import Role, Roles_enum
from app import db

@bp.route('/signup', methods=['POST'])
def signup():
    if not request.json:
        abort(400, "response should be a JSON object")
    data = request.json
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
    if not _validate(data):
        abort(400, "One or more fields required")
    
    _username = data['username']
    _password = hashlib.sha256(data['password'].encode()).hexdigest()
    _email = data['email']
    _firstname = data['firstname']
    _lastname = data['lastname']

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
    user.role.append(role)
    db.session.add(user)
    db.session.commit()

    return jsonify(user.json()), 201


@bp.route('/login', methods=['post'])
def login():
    if not request.json:
        abort(400, "response should be a JSON object")
    data = request.json
    def _validate(request) -> bool:
        if 'username' not in request and 'email' not in request:
            return False
        if 'password' not in request:
            return False
        return True
    if not _validate(data):
        abort(400, "one or more field is required")

    _password = hashlib.sha256(data['password'].encode()).hexdigest()
    def _validate_user(password) -> bool:
        if 'username' in data:
            user = User.query.filter(
                db.func.lower(User.username) == data['username'].lower()
                    ).first()
            if not user:
                return False
            if user.password == password:
                return True
            return False
        if 'email' in data:
            user = User.query.filter(
                db.func.lower(User.email) == data['email'].lower()
            ).first()

            if not user:
                return False
            if user.password == password:
                return True
            return False
    
    if not _validate_user(_password):
        abort(404, "user not found")
    return jsonify("login successful"), 201
