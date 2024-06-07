# app/controller/main_controller.py
from app.model import db
from app.model.models import User


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
