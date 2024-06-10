from datetime import timedelta
from flask import Flask
from flask_restplus import Api
from flask_cors import CORS
from app.model import init_db


def create_app():
    app = Flask(__name__)
    init_db(app)

    app.config["SECRET_KEY"] = "ala123"  # Replace with your actual secret key
    app.config["JWT_SECRET_KEY"] = "ala123"  # Replace with your actual JWT secret key
    app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
    app.config["JWT_COOKIE_CSRF_PROTECT"] = False
    app.config["JWT_COOKIE_SAMESITE"] = "None"
    app.config["JWT_COOKIE_SECURE"] = True
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=1)

    CORS(app, resources={r"/*": {"origins": "*", "supports_credentials": True}})

    api = Api(
        app, version="1.0", title="API Documentation", description="API Documentation"
    )

    from app.routes.main_routes import main_bp
    from app.routes.auth_routes import auth_bp

    api.add_namespace(main_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
