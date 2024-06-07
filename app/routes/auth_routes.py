from flask import Blueprint, request
from flask_cors import cross_origin
from app.controller.auth_controller import register_user, login_user, logout_user

auth_bp = Blueprint("auth_bp", __name__)


@auth_bp.route("/auth/register", methods=["POST"])
@cross_origin(origin="http://localhost:5173", headers=["Content-Type", "Authorization"])
def register():
    data = request.get_json()
    return register_user(data)


@auth_bp.route("/auth/login", methods=["POST"])
@cross_origin(origin="*", headers=["Content-Type", "Authorization"])
def login():
    data = request.get_json()
    return login_user(data)


@auth_bp.route("/auth/logout", methods=["POST"])
@cross_origin(origin="http://localhost:5173", headers=["Content-Type", "Authorization"])
def logout():
    return logout_user()
