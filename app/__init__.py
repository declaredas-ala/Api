# app/__init__.py
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS  # Import CORS
from app.config import DevelopmentConfig
from app.model import init_db


def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)

    # JWT configuration
    app.config["JWT_SECRET_KEY"] = (
        "your_jwt_secret_key"  # Change this to a secure secret
    )

    jwt = JWTManager(app)
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
