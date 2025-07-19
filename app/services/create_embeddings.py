from langchain_ollama.embeddings import OllamaEmbeddings

#to be able to use Ollama embeddings for text processing
#make sure to run the ollama server first
embedding_model = OllamaEmbeddings(model="llama3", base_url="http://localhost:11434")

def embed_text(text: str):
    return embedding_model.embed_query(text)
