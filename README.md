# WooChat - College of Wooster AI Chatbot

A Flask-based chatbot application that provides information about the College of Wooster using OpenAI and Pinecone vector database.

## Features

- AI-powered chatbot using OpenAI GPT models
- Vector search using Pinecone for relevant information retrieval
- Web-based interface with modern UI
- CORS-enabled for cross-origin requests

## Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables in `.env`:
```
OPENAI_API_KEY=your_openai_api_key
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_ENVIRONMENT=your_pinecone_environment
INDEX_NAME=woochat
```

3. Run the application:
```bash
python app.py
```

The app will be available at `http://localhost:5001`

## Deployment

### Render.com (Recommended for Free Tier)

1. Push your code to a GitHub repository
2. Create a new Web Service on Render.com
3. Connect your GitHub repository
4. Set the following environment variables in Render:
   - `OPENAI_API_KEY`
   - `PINECONE_API_KEY`
   - `PINECONE_ENVIRONMENT`
   - `INDEX_NAME`
5. Deploy!

### Other Platforms

The app includes:
- `requirements.txt` - Python dependencies
- `Procfile` - Process definition for deployment
- `runtime.txt` - Python version specification

## Project Structure

```
WooChat-main/
├── app.py                 # Main Flask application
├── pc_vector_store/       # Pinecone vector store integration
├── persistence/           # Memory and workflow management
├── static/               # CSS and static assets
├── templates/            # HTML templates
└── requirements.txt      # Python dependencies
```

## Technologies Used

- Flask - Web framework
- OpenAI - AI language models
- Pinecone - Vector database
- LangChain - AI framework
- HTML/CSS/JavaScript - Frontend
