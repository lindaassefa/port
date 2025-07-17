import os
from dotenv import load_dotenv
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings

load_dotenv()
index_name = os.getenv("INDEX_NAME")

# Create embeddings using OpenAI's embeddings
embeddings = OpenAIEmbeddings()

# Pulling from existing index
docsearch = PineconeVectorStore.from_existing_index(index_name, embeddings)
retriever = docsearch.as_retriever()