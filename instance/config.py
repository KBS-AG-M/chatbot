# instance/config.py

from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Flask secret key (used for sessions and encryption)
SECRET_KEY = os.environ.get('SECRET_KEY', 'super-secret-dev-key')

# Firebase Admin SDK JSON key file
FIREBASE_CREDENTIALS = os.path.join(os.path.dirname(__file__), 'firebase_credentials.json')

# Encryption key (you should store this securely in production)
ENCRYPTION_KEY = os.environ.get('ENCRYPTION_KEY', b'some-32-byte-base64-key')

# Any other config values you might need
DEBUG = True
