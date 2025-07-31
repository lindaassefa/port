from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app, resources={
    r"/*": {
        "origins": "*",  # Allow all origins
        "methods": ["GET", "POST", "OPTIONS"],  # Allow specific methods
        "allow_headers": ["Content-Type", "Authorization"]  # Allow specific headers
    }
})

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
        # Import here to avoid cold start issues
        from pc_vector_store.retriever import retriever
        from persistence.memory import workflow_app
        
        # Use the retriever to fetch a response
        config = {"configurable": {"thread_id": "abc123"}}
        result = workflow_app.invoke({"input": user_input}, config=config)
        response = result["answer"]
    except Exception as e:
        response = f"An error occurred: {str(e)}"

    return jsonify({"response": response})

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port, debug=False)