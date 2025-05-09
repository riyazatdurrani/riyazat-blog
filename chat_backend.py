import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

OPENROUTER_API_KEY = os.environ.get('OPENROUTER_API_KEY')
if not OPENROUTER_API_KEY:
    raise RuntimeError("OPENROUTER_API_KEY environment variable not set!")

PROFILE_PATH = os.path.join(os.path.dirname(__file__), 'profile.txt')

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

with open(PROFILE_PATH, 'r', encoding='utf-8') as f:
    profile_context = f.read()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)

@app.route('/chat-api', methods=['POST'])
def chat_api():
    data = request.get_json()
    user_message = data.get('message', '')
    if not user_message:
        return jsonify({'reply': "Please enter a message."})

    try:
        completion = client.chat.completions.create(
            extra_headers={},
            extra_body={},
            model="qwen/qwen3-32b:free",
            messages=[
                {"role": "system", "content": f"You are acting as Riyazat and responding on his behalf. Use the information in the file profile.txt as your only source of truth about Riyazat's background, personality, work, and preferences.\n\nProfile:\n{profile_context}"},
                {"role": "user", "content": user_message}
            ]
        )
        reply = completion.choices[0].message.content
    except Exception as e:
        reply = f"Error: {str(e)}"
    return jsonify({'reply': reply})

@app.route('/')
def home():
    return 'Riyazat Chat API is running!'

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port, debug=True)
