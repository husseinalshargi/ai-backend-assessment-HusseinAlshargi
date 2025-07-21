from app.retrieval.generate_answer import generate_answer

from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


ask_router = APIRouter()

#request model
class AskRequest(BaseModel):
    query: str
    from_date: Optional[datetime] = None
    to_date: Optional[datetime] = None
    tenant: Optional[str] = None
    file_name: Optional[str] = None
    conversation_id: Optional[str] = "default"



@ask_router.post("/chat")
def chat(request: AskRequest):
    result = generate_answer(
        query=request.query,
        from_date=request.from_date,
        to_date=request.to_date,
        tenant=request.tenant,
        file_name=request.file_name,
        conversation_id=request.conversation_id
    )
    return result

