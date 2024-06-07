from flask import jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, unset_jwt_cookies
from app.model import db
from app.model.models import User


def register_user(data):
    if not all(
        key in data for key in ("first_name", "last_name", "email", "phone", "password")
    ):
        return jsonify({"error": "Missing required fields"}), 400

    if db.session.query(User).filter_by(email=data["email"]).first():
        return jsonify({"error": "Email already registered"}), 400

    hashed_password = generate_password_hash(data["password"], method="pbkdf2:sha256")
    new_user = User(
        first_name=data["first_name"],
        last_name=data["last_name"],
        email=data["email"],
        phone=data["phone"],
        password=hashed_password,
        is_admin=data.get("is_admin", False),
        is_active=data.get(
            "is_active", True
        ),  # Consider making users active by default
    )
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201


def login_user(data):
    if not all(key in data for key in ("email", "password")):
        return jsonify({"error": "Missing required fields"}), 400

    user = db.session.query(User).filter_by(email=data["email"]).first()

    access_token = create_access_token(identity=user.id)
    response = make_response(jsonify({"message": "Login successful"}), 200)
    response.set_cookie(
        "access_token", access_token, httponly=True, secure=True, samesite="Lax"
    )

    return response


@jwt_required()
def logout_user():
    response = make_response(jsonify({"message": "Logout successful"}), 200)
    unset_jwt_cookies(response)
    response.set_cookie(
        "access_token", "", expires=0, httponly=True, secure=True, samesite="Lax"
    )
    return response
