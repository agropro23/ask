# from flask import Flask, request, jsonify
# import requests

# app = Flask(__name__)

# @app.route("/ask", methods=["POST"])
# def ask():
#     data = request.json or {}
#     prompt = data.get("prompt", "")
#     user_api_key = data.get("api_key", "").strip()

#     if not user_api_key:
#         return jsonify({"response": "Error: No API key provided."}), 400

#     try:
#         headers = {
#             "Authorization": f"Bearer {user_api_key}",
#             "Content-Type": "application/json",
#         }

#         payload = {
#             "model": "llama-3.3-70b-versatile",  # Gemini-style model on Groq
#             "messages": [
#                 {"role": "system", "content": "You are a helpful programming assistant."},
#                 {"role": "user", "content": prompt}
#             ]
#         }

#         groq_response = requests.post(
#             "https://api.groq.com/openai/v1/chat/completions",
#             headers=headers,
#             json=payload
#         )

#         # Handle Groq errors gracefully
#         if groq_response.status_code != 200:
#             return jsonify({
#                 "response": f"Groq API error ({groq_response.status_code}): {groq_response.text}"
#             }), groq_response.status_code

#         result = groq_response.json()
#         message = result["choices"][0]["message"]["content"]
#         return jsonify({"response": message})

#     except Exception as e:
#         return jsonify({"response": f"Server error: {e}"}), 500

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000)

from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json or {}
    prompt = data.get("prompt", "")
    user_api_key = data.get("api_key", "").strip()

    if not user_api_key:
        return jsonify({"response": "Error: No API key provided."}), 400

    try:
        # Google Gemini endpoint
        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent"

        headers = {
            "Content-Type": "application/json"
        }

        payload = {
            "contents": [
                {
                    "role": "user",
                    "parts": [{"text": prompt}]
                }
            ]
        }

        # Send request to Gemini API with user-provided key
        response = requests.post(
            f"{url}?key={user_api_key}",
            headers=headers,
            json=payload
        )

        # Handle Gemini errors gracefully
        if response.status_code != 200:
            return jsonify({
                "response": f"Gemini API error ({response.status_code}): {response.text}"
            }), response.status_code

        result = response.json()

        # Extract text output from Gemini’s response
        try:
            message = result["candidates"][0]["content"]["parts"][0]["text"]
        except (KeyError, IndexError):
            message = "No valid response from Gemini."

        return jsonify({"response": message})

    except Exception as e:
        return jsonify({"response": f"Server error: {e}"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
