from langchain_ollama.embeddings import OllamaEmbeddings

import os  
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file
Ollama_model = os.getenv("Ollama_model")
Ollama_base_url = os.getenv("Ollama_base_url")


#to be able to use Ollama embeddings for text processing
#make sure to run the ollama server first
embedding_model = OllamaEmbeddings(model=Ollama_model, base_url=Ollama_base_url)

def embed_text(text: str):
    return embedding_model.embed_query(text)
