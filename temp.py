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
        # --- THIS IS THE FIX ---
        # Changed model from "gemini-1.5-flash" to "gemini-2.5-pro"
        # to use the latest Pro model as requested.
        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro:generateContent"
        # ---------------------

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
            # Try to find an error message from Gemini if the format is unexpected
            error_message = result.get("error", {}).get("message", "No valid response from Gemini.")
            message = f"Error processing Gemini response: {error_message}"
            if not result.get("candidates"):
                 message = f"Gemini API returned no candidates. Full response: {result}"


        return jsonify({"response": message})

    except requests.exceptions.RequestException as e:
        # Handle network errors (e.g., DNS failure, connection refused)
        return jsonify({"response": f"Network error: {e}"}), 500
    except Exception as e:
        # Handle any other server error
        return jsonify({"response": f"Server error: {e}"}), 500


if __name__ == "__main__":
    # Use a different port like 8080 just in case 5000 is used by another service
    app.run(host="0.0.0.0", port=8080)


