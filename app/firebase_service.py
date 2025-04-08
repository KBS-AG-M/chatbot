# app/firebase_service.py

import firebase_admin
from firebase_admin import credentials, firestore, auth
import os

# Prevent multiple initializations
if not firebase_admin._apps:
    cred_path = os.path.join(os.getcwd(), "instance", "firebase_credentials.json")
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)

# Initialize Firestore
db = firestore.client()

def store_encrypted_message(user_id, chat_id, message_data):
    """
    Stores an encrypted message in Firestore under a specific user and chat ID.
    """
    ref = db.collection('users').document(user_id).collection('chats').document(chat_id).collection('messages')
    ref.add(message_data)

def get_chat_history(user_id, chat_id):
    """
    Retrieves all messages for a specific chat, ordered by timestamp.
    """
    ref = db.collection('users').document(user_id).collection('chats').document(chat_id).collection('messages')
    docs = ref.order_by('timestamp').stream()
    return [doc.to_dict() for doc in docs]

def create_new_chat(user_id):
    """
    Creates a new chat document for the user and returns its ID.
    """
    ref = db.collection('users').document(user_id).collection('chats').document()
    ref.set({'created_at': firestore.SERVER_TIMESTAMP})
    return ref.id
