# app/encryption.py
from cryptography.fernet import Fernet

# Normally this key would be loaded from secure config
KEY = Fernet.generate_key()
cipher = Fernet(KEY)

def encrypt_message(message):
    return cipher.encrypt(message.encode()).decode()

def decrypt_message(token):
    return cipher.decrypt(token.encode()).decode()
