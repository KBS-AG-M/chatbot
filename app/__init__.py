# app/__init__.py
from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)  # Enable CORS for API endpoints

    # App config
    app.config.from_pyfile('../instance/config.py')

    # Import and register routes
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
