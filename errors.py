from flask import Blueprint, jsonify

blueprint = Blueprint("errors", __name__)

@blueprint.app_errorhandler(400)
def bad_request(error):
    return jsonify(
        {
            "error": {
                "reason": "bad request",
                "message": error.description,
                "status": 400
            }
        }
    ), 400

@blueprint.app_errorhandler(401)
def unauthorized(error):
    return jsonify(
        {
            "error": {
                "reason": "unauthorized",
                "message": error.description,
                "status": 401
            }
        }
    ), 401

@blueprint.app_errorhandler(403)
def forbidden(error):
    return jsonify(
        {
            "error": {
                "reason": "forbidden",
                "message": error.description,
                "status": 403
            }
        }
    ), 403


@blueprint.app_errorhandler(404)
def not_found(error):
    return jsonify(
        {
            "error": {
                "reason": "not found",
                "message": error.description,
                "status": 404
            }
        }
    ), 404


@blueprint.app_errorhandler(409)
def conflict(error):
    return jsonify(
        {
            "error": {
                "reason": "conflict",
                "message": error.description,
                "status": 409
            }
        }
    ), 409

@blueprint.app_errorhandler(500)
def internal_error(error):
    return jsonify(
        {
            "error": {
                "reason": "enternal error",
                "message": error.description,
                "status": 500
            }
        }
    ), 500