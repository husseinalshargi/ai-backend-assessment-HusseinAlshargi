from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate

import os  
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file
Ollama_model = os.getenv("Ollama_model")
Ollama_base_url = os.getenv("Ollama_base_url")

#make sure to run the ollama server first
llm = OllamaLLM(model=Ollama_model, base_url=Ollama_base_url)

#prompt template for generating summaries
prompt_template = PromptTemplate.from_template("""
You are a summarizer assistant.

Summarize the following conversation into a short, clear summary of what has been discussed so far. Include main topics, questions, and assistant responses.

Conversation:
{conversation}

Summary:
""")


def generate_summary(chat_history): #chat history is a list of messages (dicts with 'role' and 'message' keys)

    #check if there are any messages in the chat history provided
    if len(chat_history) == 0:
        return "No conversation history to summarize."
    
    #format the chat history into a string with roles and messages
    conversation = "\n".join([f"{message['role'].capitalize()}: {message['message']}" for message in chat_history])


    #create a chain that combines the prompt template with the LLM
    qa_chain = prompt_template | llm
    
    # Generate the summary using the chain
    summary = qa_chain.invoke({"conversation": conversation})

    return summary
    


