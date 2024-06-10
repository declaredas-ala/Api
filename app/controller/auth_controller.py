from flask import jsonify, make_response, request
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    set_access_cookies,
    unset_jwt_cookies,
    get_jwt_identity,
    verify_jwt_in_request,
)
from app.model import db
from app.model.models import User
import bcrypt


def register_user(data):
    if not all(
        key in data for key in ("first_name", "last_name", "email", "phone", "password")
    ):
        return jsonify({"error": "Missing required fields"}), 400

    if db.session.query(User).filter_by(email=data["email"]).first():
        return jsonify({"error": "Email already registered"}), 400

    hashed_password = bcrypt.hashpw(data["password"].encode("utf-8"), bcrypt.gensalt())
    new_user = User(
        first_name=data["first_name"],
        last_name=data["last_name"],
        email=data["email"],
        phone=data["phone"],
        password=hashed_password.decode("utf-8"),
        is_admin=data.get("is_admin", False),
        is_active=data.get("is_active", False),  # Setting is_active to 0 by default
    )
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201


def login_user(data):
    if not all(key in data for key in ("email", "password")):
        return jsonify({"error": "Missing required fields"}), 400

    user = db.session.query(User).filter_by(email=data["email"]).first()

    if user is None:
        return jsonify({"error": "Invalid email or password"}), 401

    if not bcrypt.checkpw(
        data["password"].encode("utf-8"), user.password.encode("utf-8")
    ):
        return jsonify({"error": "Invalid email or password"}), 401

    # Create access token
    access_token = create_access_token(identity=user.id)

    # Construct response data
    response_data = {
        "fullName": f"{user.first_name} {user.last_name}",
        "email": user.email,
        "phone": user.phone,
        "role": "Admin" if user.is_admin else "User",
        "isActive": user.is_active,
    }

    # Set the token in a cookie
    response = make_response(jsonify(response_data), 200)

    set_access_cookies(response, access_token)

    return response


@jwt_required(locations=["cookies"])
def logout_user():
    response = make_response(jsonify({"message": "Logout successful"}), 200)
    # Clearing all cookies
    response.delete_cookie("access_token_cookie")
    unset_jwt_cookies(response)
    return response


@jwt_required(locations=["cookies"])
def get_profile():
    access_token = request.cookies.get("access_token_cookie")
    if not access_token:
        return jsonify({"error": "Missing Access Token"}), 401
    print(access_token)

    user_id = get_jwt_identity()
    user = db.session.query(User).get(user_id)
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
    ), 200


@jwt_required()
def update_profile():
    access_token = request.cookies.get("access_token_cookie")
    if not access_token:
        return jsonify({"error": "Missing Access Token"}), 401

    user_id = get_jwt_identity()
    user = db.session.query(User).get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json()

    user.first_name = data.get("first_name", user.first_name)
    user.last_name = data.get("last_name", user.last_name)
    user.email = data.get("email", user.email)
    user.phone = data.get("phone", user.phone)
    user.is_admin = data.get("is_admin", user.is_admin)
    user.is_active = data.get("is_active", user.is_active)

    db.session.commit()

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
    ), 200
