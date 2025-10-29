from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json or {}
    prompt = data.get("prompt", "")
    api_key = data.get("api_key", "")

    # Optional: simple API key check (or remove this if not needed)
    if api_key and api_key != "your_local_dummy_key":
        return jsonify({"response": "Invalid API key."}), 403

    try:
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": "gemma2-9b-it",
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        }

        r = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=payload
        )

        if r.status_code != 200:
            return jsonify({"response": f"Groq API error: {r.text}"}), 500

        result = r.json()
        message = result["choices"][0]["message"]["content"]
        return jsonify({"response": message})

    except Exception as e:
        return jsonify({"response": f"Server error: {e}"})
