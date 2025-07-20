from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from app.services.retrive_documents import retrieve_relevant_chunks

import os  
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file
Ollama_model = os.getenv("Ollama_model")
Ollama_base_url = os.getenv("Ollama_base_url")


#to be able to use Ollama embeddings for text processing
#make sure to run the ollama server first
llm = OllamaLLM(model=Ollama_model, base_url=Ollama_base_url)

#define a prompt template for generating answers
prompt_template = PromptTemplate.from_template("""
You are a helpful assistant. Use the following document context to answer the question.

Context:
{context}

Question: {question}

Answer:
""")


#create a chain that combines the prompt template with the LLM
qa_chain = prompt_template | llm

#function to generate an answer based on a query
def generate_answer(query, top_k=3, from_date=None, to_date=None, tenant=None, file_name=None):
    
    relevant_chunks = retrieve_relevant_chunks(query, top_k=top_k, 
                                                from_date=from_date, 
                                                to_date=to_date, 
                                                tenant=tenant, 
                                                file_name=file_name)
    context = "\n\n".join(relevant_chunks)
    # Run the chain with .invoke() and pass variables as a dict
    return qa_chain.invoke({"context": context, "question": query})
