from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv

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

# Lazy loading of heavy dependencies
def get_workflow_app():
    """Lazy load the workflow app to avoid cold start issues."""
    from persistence.memory import workflow_app
    return workflow_app

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
        # Lazy load the workflow app
        workflow_app = get_workflow_app()
        
        # Use the retriever to fetch a response
        config = {"configurable": {"thread_id": "abc123"}}
        result = workflow_app.invoke({"input": user_input}, config=config)
        response = result["answer"]
    except Exception as e:
        response = f"An error occurred: {str(e)}"

    return jsonify({"response": response})

# For Vercel serverless
app.debug = False 