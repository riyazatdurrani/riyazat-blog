import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI

OPENROUTER_API_KEY = os.environ.get('OPENROUTER_API_KEY', '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')
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
            extra_headers={
                # Optionally set these for OpenRouter ranking
                # "HTTP-Referer": "http://localhost:5001", 
                # "X-Title": "Riyazat Blog Chatbot",
            },
            extra_body={},
            model="qwen/qwen3-32b:free",
            messages=[
                {"role": "system", "content": f"You are acting as Riyazat and responding on his behalf. Use the information in the file profile.txt as your only source of truth about Riyazat's background, personality, work, and preferences. Always keep your responses brief, clear, and casual—just like a real person replying in conversation. Never sound like an AI. Avoid robotic, overly formal, or explanatory answers. If you don’t know the answer or if it's not in the profile, say something like “Not sure about that” or “I’ll have to check and get back.” Stay in character and keep it real. No made-up facts or filler. Use the following profile to answer as yourself.\n{profile_context}"},
                {"role": "user", "content": user_message}
            ]
        )
        reply = completion.choices[0].message.content
    except Exception as e:
        reply = f"Error: {str(e)}"
    return jsonify({'reply': reply})

if __name__ == '__main__':
    app.run(port=5001, debug=True)
