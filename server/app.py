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

CORS(app, resources={r"/*": {"origins": "https://bing-ai-clone.netlify.app"}})

# Add CORS headers to every response
@app.after_request
def add_cors_headers(response):
    response.headers.add('Access-Control-Allow-Origin', 'https://bing-ai-clone.netlify.app')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

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
