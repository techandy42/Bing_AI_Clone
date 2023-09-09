from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
from search import generate_prompt_with_results
from chatbot import get_chat_completion, fetch_and_answer
from extract import extract_urls

# Load variables from .env
load_dotenv()

# Initialize the Flask application
app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

# Define routes
@app.route('/')
def hello_world():
    return jsonify({"message": "Hello! This is the Bing AI Clone server."})

@app.route('/search', methods=['POST'])
def search():
    data = request.get_json()  # Parse JSON payload
    query = data.get('query', '')  # Get 'query', default is an empty string
    prompt = generate_prompt_with_results(query)
    chatbot_response = get_chat_completion(prompt)
    return jsonify({"message": chatbot_response})

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()  # Parse JSON payload
    search_chatbot_result = data.get('search_chatbot_result', '')
    user_input = data.get('user_input', '')
    extracted_links = extract_urls(search_chatbot_result)
    chatbot_response = fetch_and_answer(extracted_links, user_input)
    return jsonify({"message": chatbot_response})

# Run the application
if __name__ == '__main__':
    app.run(debug=True)

