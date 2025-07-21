import time
from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate
from app.services.memory import store_message
from app.retrieval.retrive_documents import retrieve_relevant_chunks

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
def generate_answer(query, top_k=3, from_date=None, to_date=None, tenant=None, file_name=None, conversation_id='default'):
    start_time = time.time()

    #add the message to the short term memory
    role = "user"  #the role is user for the query
    store_message(conversation_id, role, query)

    #retrieve relevant chunks based on the query and filters, it will retreve a list of dict with two values text and score
    relevant_chunks = retrieve_relevant_chunks(query, top_k=top_k, 
                                                from_date=from_date, 
                                                to_date=to_date, 
                                                tenant=tenant, 
                                                file_name=file_name)
    
    if not relevant_chunks:
        return {
            "conversation_id": conversation_id,
            "answer": "No relevant documents found",
            "sources": [],
            "latency_ms": int((time.time() - start_time) * 1000),
            "tokens_in": 0,
            "tokens_out": 0
        }
    else:
        context = "\n".join(chunk["text"] for chunk in relevant_chunks)
        sources = [
            {
                "source": chunk.get("file_name", ""),
                "score": round(chunk.get("score", 0.0), 2)
            }
            for chunk in relevant_chunks
        ]


        response = qa_chain.invoke({"context": context, "question": query})

        tokens_in = len(context.split()) + len(query.split())  
        tokens_out = len(str(response).split())

    #add the response to the short term memory
    role = "assistant"  #the role is assistant for the response
    store_message(conversation_id, role, response)
    
    #run the chain with .invoke() and pass variables as a dict
    #return structured output
    return {
        "conversation_id": conversation_id,
        "answer": response,
        "sources": sources,
        "latency_ms": int((time.time() - start_time) * 1000),
        "tokens_in": tokens_in,
        "tokens_out": tokens_out
    }
