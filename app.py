# from flask import Flask, render_template, request, jsonify
# import os
# from dotenv import load_dotenv
# import requests
# import logging

# # .env dosyasındaki çevresel değişkenleri yükle
# load_dotenv()

# # API Key'i .env dosyasından al
# GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# # Flask uygulamasını başlat
# app = Flask(__name__)
# app.config['DEBUG'] = True  # Debugging aktif

# # Logging configuration
# logging.basicConfig(level=logging.DEBUG)
# logger = logging.getLogger(__name__)

# # Ana sayfayı render et
# @app.route('/')
# def index():
#     return render_template('index.html')  # index.html dosyasını render et

# # Groq API'sine POST isteği atmak için kullanılan endpoint
# @app.route('/ask', methods=['POST'])
# def ask():
#     try:
#         user_input = request.json['user_input']  # Kullanıcının girdiği veriyi al
#         logger.debug(f"User input received: {user_input}")

#         # Groq API'sine yanıt almak için istek gönder
#         response = get_groq_response(user_input)

#         if response:
#             return jsonify({"response": response})
#         else:
#             logger.error("No response received from Groq API")
#             return jsonify({"error": "An error occurred while processing the request."}), 500
#     except Exception as e:
#         logger.error(f"An error occurred: {e}")
#         return jsonify({"error": str(e)}), 500

# # Groq API'ye istek gönderme fonksiyonu
# def get_groq_response(query):
#     url = "https://api.groq.com/openai/v1/chat/completions"  # Groq API endpoint
#     headers = {
#         "Authorization": f"Bearer {GROQ_API_KEY}",
#         "Content-Type": "application/json"
#     }
#     payload = {
#         "model": "llama-3.3-70b-versatile",  # Kullanılacak model
#         "messages": [{"role": "user", "content": query}]  # Kullanıcının girdiği sorgu
#     }

#     try:
#         logger.debug(f"Sending request to Groq API: URL={url}, Headers={headers}, Payload={payload}")
#         response = requests.post(url, headers=headers, json=payload)
#         logger.debug(f"API Response Status Code: {response.status_code}")
#         logger.debug(f"API Response Body: {response.text}")

#         if response.status_code == 200:
#             response_data = response.json()
#             return response_data.get('choices', [{}])[0].get('message', {}).get('content', "No response found")
#         else:
#             logger.error(f"API Error: {response.status_code} - {response.text}")
#             return None
#     except Exception as e:
#         logger.error(f"Error in get_groq_response: {e}")
#         return None

# if __name__ == '__main__':
#     app.run(debug=True, port=5001)