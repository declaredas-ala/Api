from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from app.controller.auth_controller import login_user, logout_user, register_user

auth_bp = Blueprint("auth_bp", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    response, status_code = register_user(data)
    return response, status_code


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    response = login_user(data)
    return response


@jwt_required(locations=["cookies"])
@auth_bp.route("/logout", methods=["POST"])
def logout():
    return logout_user()
