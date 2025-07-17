import os
from langchain_openai import ChatOpenAI 
from dotenv import load_dotenv
load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(  
    openai_api_key=openai_api_key,  
    model_name='gpt-3.5-turbo',  
    temperature=0.0  
)  
