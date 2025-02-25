import requests
import logging
from datetime import datetime
from functools import lru_cache

# Logging configuration
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def get_groq_response(query):
    """
    Groq API'sine istek gönderir ve yanıtı döndürür.
    """
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

@lru_cache(maxsize=100)
def cached_groq_response(query):
    """
    Sık kullanılan sorguları önbelleğe alır.
    """
    return get_groq_response(query)

def validate_input(input_text):
    """
    Kullanıcı girdisini doğrular.
    """
    if not input_text or len(input_text.strip()) == 0:
        return False
    return True

def log_api_request(endpoint, request_data, response_data, status_code):
    """
    API isteklerini loglar.
    """
    log_entry = {
        "endpoint": endpoint,
        "request_data": request_data,
        "response_data": response_data,
        "status_code": status_code,
        "timestamp": datetime.utcnow()
    }
    logger.info(f"API Request Log: {log_entry}")