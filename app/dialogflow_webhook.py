# app/dialogflow_webhook.py
from flask import Blueprint, request, jsonify

dialogflow_webhook = Blueprint('dialogflow_webhook', __name__)

@dialogflow_webhook.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json()
    query = req['queryResult']['queryText']
    
    # You can connect this with your NLTK FAQ engine too.
    response = {
        "fulfillmentText": f"You said: {query}"
    }
    
    return jsonify(response)
