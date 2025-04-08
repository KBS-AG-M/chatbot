# app/routes.py
from flask import Blueprint, render_template, redirect, url_for, session, request, jsonify
import firebase_admin
from firebase_admin import auth
from app.faq_engine import FAQEngine

main = Blueprint('main', __name__)

faq_engine = FAQEngine(dataset_path='data/faq_dataset.csv')

@main.route('/')
def index():
    return render_template('login.html')

@main.route('/chat')
def chat():
    # Check if the user is logged in
    if 'user_id' not in session:
        return redirect(url_for('main.index'))
    
    # Pass user information to the chat page
    user_email = session.get('user_email', 'Guest')
    return render_template('index.html', user_email=user_email)

@main.route('/logout')
def logout():
    # Clear the session and redirect to the login page
    session.clear()
    return redirect(url_for('main.index'))

@main.route('/verify-token', methods=['POST'])
def verify_token():
    try:
        data = request.get_json()
        id_token = data.get('idToken')

        # Verify the token with Firebase Admin SDK
        decoded_token = auth.verify_id_token(id_token)
        user_id = decoded_token['uid']
        user_email = decoded_token.get('email')

        # Save user ID and email to session
        session['user_id'] = user_id
        session['user_email'] = user_email

        return jsonify({"success": True, "user": user_email})
    except Exception as e:
        print(e)
        return jsonify({"success": False}), 401

@main.route('/get', methods=['POST'])
def get_response():
    try:
        data = request.get_json()
        user_message = data.get('message', '')

        # Use the FAQ engine to get a response
        bot_response = faq_engine.get_answer(user_message)

        return jsonify({"response": bot_response})
    except Exception as e:
        print(f"Error in /get endpoint: {e}")
        return jsonify({"response": "Sorry, something went wrong."}), 500