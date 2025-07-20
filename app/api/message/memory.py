from fastapi import APIRouter
from app.services.memory import store_message, get_context, store_summary, get_summaries

message_router = APIRouter()

@message_router.post("/store_message/")
def store_message_endpoint(conversation_id, role, message):
    store_message(conversation_id, role, message)
    return {"status": "Message stored successfully"}

@message_router.get("/get_context/")
def get_context_endpoint(conversation_id):
    context = get_context(conversation_id)
    return {"context": context}

@message_router.post("/store_summary/")
def store_summary_endpoint(conversation_id, summary, turn_number):
    store_summary(conversation_id, summary, turn_number)
    return {"status": "Summary stored successfully"}

@message_router.get("/get_summaries/")
def get_summaries_endpoint(conversation_id):
    summaries = get_summaries(conversation_id)
    return {"summaries": summaries}