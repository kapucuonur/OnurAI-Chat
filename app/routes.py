from flask import Blueprint, render_template, request, jsonify
import requests
import os
import logging

# Blueprint oluştur
main_bp = Blueprint('main', __name__)

# Logging configuration
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Ana sayfa
@main_bp.route('/')
def index():
    return render_template('index.html')

# Groq API'sine istek gönderme
@main_bp.route('/ask', methods=['POST'])
def ask():
    try:
        user_input = request.json['user_input']
        logger.debug(f"User input received: {user_input}")

        # Groq API'sine istek gönder
        response = get_groq_response(user_input)

        if response:
            return jsonify({"response": response})
        else:
            logger.error("No response received from Groq API")
            return jsonify({"error": "An error occurred while processing the request."}), 500
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return jsonify({"error": str(e)}), 500

# Groq API'ye istek gönderme fonksiyonu
def get_groq_response(query):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {os.getenv('GROQ_API_KEY')}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": query}]
    }

    try:
        logger.debug(f"Sending request to Groq API: URL={url}, Headers={headers}, Payload={payload}")
        response = requests.post(url, headers=headers, json=payload)
        logger.debug(f"API Response Status Code: {response.status_code}")
        logger.debug(f"API Response Body: {response.text}")

        if response.status_code == 200:
            response_data = response.json()
            return response_data.get('choices', [{}])[0].get('message', {}).get('content', "No response found")
        else:
            logger.error(f"API Error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        logger.error(f"Error in get_groq_response: {e}")
        return None