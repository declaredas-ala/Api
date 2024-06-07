from flask import Flask
from flask_restplus import Api
from flask_cors import CORS
from app.model import init_db


def create_app():
    app = Flask(__name__)
    init_db(app)
    api = Api(
        app, version="1.0", title="API Documentation", description="API Documentation"
    )

    # Enable CORS for the specified origin
    CORS(app, resources={r"/*": {"origins": "http://localhost:5173/*"}})

    # Import and register your routes here
    from app.routes.main_routes import main_bp

    api.add_namespace(main_bp)

    return app
