from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app, resources={
    r"/*": {
        "origins": "*",
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# Configure OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/")
def home():
    """Render the chatbot interface."""
    return render_template("index.html")

@app.route("/query", methods=["POST", "OPTIONS"])
def query():
    """Handle user input and return AI-generated responses."""
    # Handle preflight requests
    if request.method == "OPTIONS":
        return "", 200
        
    user_input = request.json.get("message", "") if request.json else ""

    if not user_input:
        return jsonify({"response": "Please enter a message to proceed."})

    try:
        # Use OpenAI directly
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant for the College of Wooster. Provide accurate information about the college, its programs, campus life, and policies. If you don't know something specific about Wooster, say so."},
                {"role": "user", "content": user_input}
            ],
            max_tokens=500,
            temperature=0.7
        )
        
        ai_response = response.choices[0].message.content
    except Exception as e:
        print(f"Error in query: {e}")
        ai_response = f"An error occurred: {str(e)}"

    return jsonify({"response": ai_response})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port, debug=False) 