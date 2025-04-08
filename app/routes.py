# app/routes.py
from flask import Blueprint, render_template, redirect, url_for, session, request, jsonify
import firebase_admin
from firebase_admin import auth

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('login.html')

@main.route('/chat')
def chat():
    # Simulated logged-in check
    if 'user_id' not in session:
        return redirect(url_for('main.index'))
    return render_template('index.html')

@main.route('/logout')
def logout():
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

        # Save user ID to session
        session['user_id'] = user_id
        session['user_email'] = user_email

        return jsonify({"success": True, "user": user_email})
    except Exception as e:
        print(e)
        return jsonify({"success": False}), 401