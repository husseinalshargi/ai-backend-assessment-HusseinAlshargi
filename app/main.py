# a library that run cli commands which run tasks from the terminal without needing the user to write all the code 
import typer
from fastapi import FastAPI
from contextlib import asynccontextmanager #to handle both start up and shutdown
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from app.api.report.generate import generate_router
from app.schemas.create_db_tables import create_tables
from app.scripts.create_api_key import create_api_key
from app.services.ingestion import ingest_files
from app.services.evaluation import evaluate_answer
from app.api.admin.Scheduler import scheduler_router
from app.api.ask import ask_router
from app.api.train_document import train_router
from app.middleware.api_key_auth import APIKeyMiddleware

typer_app = typer.Typer()
scheduler = AsyncIOScheduler()


#include report generator router to the FastAPI app

@asynccontextmanager
async def lifespan(app: FastAPI):
    #start up by Adding scheduled jobs and start the scheduler
    scheduler.add_job(ingest_files, CronTrigger(hour=2, minute=0), id="nightly_refresh") #on 24-hours not 12-hours based
    scheduler.add_job(evaluate_answer, CronTrigger(hour=3, minute=0), id="nightly_evaluation")
    scheduler.start()
    print("Scheduler started.")

    yield  #run the app

    #shutdown
    scheduler.shutdown()
    print("Scheduler shut down.")


api_app = FastAPI(lifespan=lifespan) #added the function to the api obj so that it starts and shuted down with it
api_app.include_router(generate_router, prefix="/api/report")
api_app.include_router(scheduler_router, prefix='/api/admin')
api_app.include_router(ask_router, prefix='/api')
api_app.include_router(train_router, prefix='/api')

#to add the middelware of admin to the api obj
api_app.add_middleware(APIKeyMiddleware)

#CLI commands:

#in order to run it in the cli like "python -m app.main nightly-refresh" if the bool is true then add "--now" Note: we are using - not _, also we used main instead of main.py in order to be able to import a file from the same directory whithout issues
@typer_app.command()
def nightly_refresh(now : bool = False):
    if (now) : 
        ingest_files()

@typer_app.command()
def create_tables_in_db():
    create_tables()

@typer_app.command()
def evaluate():
    evaluate_answer()

@typer_app.command()
def create_an_api_key(role: str, owner_email: str):
    if role and owner_email.strip():
        create_api_key(role, owner_email)
    else:
        print("you should include both role and email")
    


if __name__ == "__main__":
    typer_app()

    