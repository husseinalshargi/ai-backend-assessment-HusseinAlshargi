from fastapi import APIRouter

from app.services.evaluation import evaluate_answer
from app.services.ingestion import ingest_files


scheduler_router = APIRouter()

@scheduler_router.post("/refresh/")
def refresh():
    ingest_files()


@scheduler_router.post("/evaluate/")
def evaluate():
    evaluate_answer()
