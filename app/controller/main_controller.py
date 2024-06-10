# app/controller/main_controller.py
from flask import request, jsonify
from app.model import db
from app.model.models import User
import jwt

# Secret key used to decode the access token (ensure this matches your JWT secret)
SECRET_KEY = "your_jwt_secret_key"


# Create a new user
def create_user(data):
    new_user = User(
        first_name=data["first_name"],
        last_name=data["last_name"],
        email=data["email"],
        phone=data["phone"],
        password=data["password"],
        is_admin=data.get("is_admin", False),
        is_active=data.get("is_active", False),
    )
    db.session.add(new_user)
    db.session.commit()
    return new_user


# Retrieve all users
def get_all_users():
    return db.session.query(User).all()


# Retrieve a user by id
def get_user_by_id(user_id):
    return db.session.query(User).get(user_id)


# Update a user
def update_user(user_id, data):
    user = db.session.query(User).get(user_id)
    if user:
        user.first_name = data.get("first_name", user.first_name)
        user.last_name = data.get("last_name", user.last_name)
        user.email = data.get("email", user.email)
        user.phone = data.get("phone", user.phone)
        user.password = data.get("password", user.password)
        user.is_admin = data.get("is_admin", user.is_admin)
        user.is_active = data.get("is_active", user.is_active)
        db.session.commit()
        return user
    else:
        return None


# Delete a user
def delete_user(user_id):
    user = db.session.query(User).get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return True
    else:
        return False


def activate_user(user_id):
    user = db.session.query(User).get(user_id)
    if user:
        user.is_active = True
        db.session.commit()
        return user
    else:
        return None


# Extract user ID from access token
def get_user_id_from_token():
    token = request.cookies.get("access_token")
    if not token:
        return None
    try:
        payload = jwt.decode(token, "ala123", algorithms=["HS256"])
        return payload.get("user_id")
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


# Get user profile
def get_profile():
    user_id = get_user_id_from_token()
    if user_id:
        user = get_user_by_id(user_id)
        if user:
            return jsonify(
                {
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email": user.email,
                    "phone": user.phone,
                    "is_admin": user.is_admin,
                    "is_active": user.is_active,
                }
            ), 200
    return jsonify({"message": "User not found or invalid token"}), 404


# Update user profile
def update_profile(data):
    user_id = get_user_id_from_token()
    if user_id:
        user = update_user(user_id, data)
        if user:
            return jsonify(
                {
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email": user.email,
                    "phone": user.phone,
                    "is_admin": user.is_admin,
                    "is_active": user.is_active,
                }
            ), 200
    return jsonify({"message": "User not found or invalid token"}), 404
