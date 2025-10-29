from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Set your Groq API key as an environment variable in Render
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    prompt = data.get("prompt", "")

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "gemma2-9b-it",  # Gemini-style model on Groq
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers=headers,
        json=payload
    )

    if response.status_code != 200:
        return jsonify({"error": response.text}), response.status_code

    result = response.json()
    message = result["choices"][0]["message"]["content"]

    return jsonify({"response": message})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
