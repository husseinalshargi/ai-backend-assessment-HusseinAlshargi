# a library that run cli commands which run tasks from the terminal without needing the user to write all the code 
import typer
from fastapi import FastAPI
from contextlib import asynccontextmanager #to handle both start up and shutdown
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from app.api.report.generate import generate_router
from app.schemas.create_db_tables import create_tables
from app.services.ingestion import ingest_files
from app.services.evaluation import evaluate_answer
from app.api.Scheduler import scheduler_router

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
api_app.include_router(scheduler_router, prefix='/api')

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
    


if __name__ == "__main__":
    typer_app()

    