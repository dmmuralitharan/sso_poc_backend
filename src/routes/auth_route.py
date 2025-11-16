from flask import Blueprint
from src.controllers.auth_controller import (
# fetch_user_by_uid_controller,
login_user_controller,
register_user_controller, 
)
auth_bp = Blueprint("auth", __name__, url_prefix="/api/v1/auth")


# Register route
@auth_bp.route("/register", methods=["POST"])
def register():
    return register_user_controller()


# Login route
@auth_bp.route("/login", methods=["POST"])
def login():
    return login_user_controller()

# Fetch current user by UID 
# @auth_bp.route("/users/<string:uid>", methods=["POST"])
# def fetch_user_by_uid(uid):
#     return fetch_user_by_uid_controller(uid)

# Fetch current user by UID 
# @auth_bp.route("/users/current_user>", methods=["POST"])
# def fetch_user_by_uid():
#     return fetch_user_by_uid_controller()


# @user_bp.route("/", methods=["GET"])
# @token_required
# def get_user(decoded_payload):
#     return get_user_controller()
