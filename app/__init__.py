# app/__init__.py
from flask import Flask
import firebase_admin
from firebase_admin import credentials
import os

def create_app():
    app = Flask(__name__)

    # Load configuration
    app.config.from_pyfile('../instance/config.py')

    # Initialize Firebase Admin SDK
    if not firebase_admin._apps:
        cred = credentials.Certificate(app.config['FIREBASE_CREDENTIALS'])
        firebase_admin.initialize_app(cred)

    # Register blueprints
    from .routes import main
    app.register_blueprint(main)

    return app
