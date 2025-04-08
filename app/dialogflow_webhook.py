# app/dialogflow_webhook.py
from flask import Blueprint, request, jsonify

dialogflow_webhook = Blueprint('dialogflow_webhook', __name__)

@dialogflow_webhook.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json()
    intent = req['queryResult']['intent']['displayName']
    query = req['queryResult']['queryText']
    
    # Handle intents
    if intent == "Default Welcome Intent":
        response_text = "Hello! How can I assist you today?"
    elif intent == "FAQ":
        response_text = f"You asked: {query}. Let me find that information for you."
    else:
        response_text = "Sorry, I didn't understand that. Can you rephrase?"

    response = {
        "fulfillmentText": response_text
    }
    
    return jsonify(response)
