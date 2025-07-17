# Add data to the Vector store from sitemap
import os
from langchain_community.document_loaders.sitemap import SitemapLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from dotenv import load_dotenv

load_dotenv()

# Load data from the College of Wooster website
loader = SitemapLoader("https://wooster.edu/sitemap-misc.xml")
documents = loader.load()

# Split the text from the documents into smaller chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1200,
    chunk_overlap=200,
    length_function=len,
)

docs = text_splitter.split_documents(documents)

# Create embeddings using OpenAI's embeddings
embeddings = OpenAIEmbeddings()
index_name = os.getenv("INDEX_NAME")

# First time
# vectorstore_from_docs = PineconeVectorStore.from_documents(
#   docs,
#   index_name=index_name,
#   embedding=embeddings
# )

vectorstore = PineconeVectorStore(index_name=index_name, embedding=embeddings)
vectorstore.add_documents(docs)