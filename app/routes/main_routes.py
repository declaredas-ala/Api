# app/routes/main_routes.py
from flask import Blueprint, jsonify, request
from app.controller.main_controller import (
    get_all_users,
    get_user_by_id,
    create_user,
    update_user,
    delete_user,
    activate_user,
)

main_bp = Blueprint("main_bp", __name__)


@main_bp.route("/users/", methods=["GET"])
def list_users():
    users = get_all_users()
    users_list = [
        {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "phone": user.phone,
            "is_admin": user.is_admin,
            "is_active": user.is_active,
            "pass": user.password,
        }
        for user in users
    ]
    return jsonify(users_list)


@main_bp.route("/users/<int:user_id>/", methods=["GET"])
def get_user_route(user_id):
    user = get_user_by_id(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(
        {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "phone": user.phone,
            "is_admin": user.is_admin,
            "is_active": user.is_active,
        }
    )


@main_bp.route("/users/", methods=["POST"])
def create_user_route():
    data = request.get_json()
    new_user = create_user(data)
    return jsonify(
        {
            "id": new_user.id,
            "first_name": new_user.first_name,
            "last_name": new_user.last_name,
            "email": new_user.email,
            "phone": new_user.phone,
            "is_admin": new_user.is_admin,
            "is_active": new_user.is_active,
        }
    ), 201


@main_bp.route("/users/<int:user_id>/", methods=["PUT"])
def update_user_route(user_id):
    data = request.get_json()
    updated_user = update_user(user_id, data)
    if not updated_user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(
        {
            "id": updated_user.id,
            "first_name": updated_user.first_name,
            "last_name": updated_user.last_name,
            "email": updated_user.email,
            "phone": updated_user.phone,
            "is_admin": updated_user.is_admin,
            "is_active": updated_user.is_active,
        }
    )


@main_bp.route("/users/<int:user_id>/", methods=["DELETE"])
def delete_user_route(user_id):
    deleted_user = delete_user(user_id)
    if not deleted_user:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"message": "User deleted"})


@main_bp.route("/users/<int:user_id>/activate", methods=["PUT"])
def activate_user_route(user_id):
    activated_user = activate_user(user_id)
    if activated_user:
        return jsonify(
            {
                "id": activated_user.id,
                "first_name": activated_user.first_name,
                "last_name": activated_user.last_name,
                "email": activated_user.email,
                "phone": activated_user.phone,
                "is_admin": activated_user.is_admin,
                "is_active": activated_user.is_active,
            }
        )
    else:
        return jsonify({"error": "User not found"}), 404
