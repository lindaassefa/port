import os
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv
from langchain_community.document_loaders.sitemap import SitemapLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore

load_dotenv()

# Initialize Pinecone with new API
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

index_name = os.getenv("INDEX_NAME")
# Extract region from PINECONE_ENVIRONMENT (e.g., 'gcp-starter' -> 'starter')
pinecone_env = os.getenv("PINECONE_ENVIRONMENT")
if pinecone_env and '-' in pinecone_env:
    _, region = pinecone_env.split('-')
else:
    region = pinecone_env or 'starter'

# Delete existing index if it exists
try:
    pc.delete_index(index_name)
    print(f"Deleted existing index: {index_name}")
except Exception as e:
    print(f"Index {index_name} does not exist or could not be deleted: {e}")

# Create new index with correct dimensions (1536 for OpenAI embeddings)
pc.create_index(
    name=index_name,
    dimension=1536,
    metric="cosine",
    spec=ServerlessSpec(
        cloud="gcp",
        region=region
    )
)
print(f"Created new index: {index_name} with dimension 1536 in gcp-{region}")

# Wait for index to be ready
import time
time.sleep(10)

# Load data from the College of Wooster website
print("Loading data from College of Wooster website...")
loader = SitemapLoader("https://wooster.edu/sitemap-misc.xml")
documents = loader.load()
print(f"Loaded {len(documents)} documents")

# Split the text from the documents into smaller chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1200,
    chunk_overlap=200,
    length_function=len,
)

docs = text_splitter.split_documents(documents)
print(f"Split into {len(docs)} chunks")

# Create embeddings using OpenAI's embeddings
embeddings = OpenAIEmbeddings()

# Add documents to the new index
print("Adding documents to Pinecone index...")
vectorstore = PineconeVectorStore(index_name=index_name, embedding=embeddings)
vectorstore.add_documents(docs)
print("Successfully added documents to Pinecone index!")

print(f"Your WooChat is now ready! Index '{index_name}' has been created with the correct dimensions.") 