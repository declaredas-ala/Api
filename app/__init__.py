# app/__init__.py
from datetime import timedelta
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS  # Import CORS
from app.config import DevelopmentConfig
from app.model import init_db


def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)

    # JWT configuration
    app.config["JWT_SECRET_KEY"] = "ala123"  # Change this to a secure secret
    app.config["SECRET_KEY"] = "ala123"  # Replace with your actual secret key
    app.config["JWT_SECRET_KEY"] = "ala123"  # Replace with your actual JWT secret key
    app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
    app.config["JWT_COOKIE_CSRF_PROTECT"] = False
    app.config["JWT_COOKIE_SECURE"] = True  # Ensures cookies are sent over HTTPS
    app.config["JWT_COOKIE_SAMESITE"] = "None"  # 'None' allows cross-site requests
    app.config["JWT_COOKIE_HTTPONLY"] = True  # Prevents JavaScript access to cookies
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=1)

    jwt = JWTManager(app)

    # Configure JWT to allow cookies for token transmission
    jwt._cookie_set = True
    init_db(app)

    from app.routes.main_routes import main_bp
    from app.routes.auth_routes import auth_bp
    from app.routes.api_call_routes import api_call_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(api_call_bp)

    # Enable CORS for all domains on all routes
    CORS(app, supports_credentials=True)

    return app
