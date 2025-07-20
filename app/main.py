# a library that run cli commands which run tasks from the terminal without needing the user to write all the code 
import typer
from fastapi import FastAPI

from app.routers import memory
from app.schemas.create_db_tables import create_tables
from app.services.ingestion import ingest_files

typer_app = typer.Typer()
api_app = FastAPI()

#include memory router to the FastAPI app
api_app.include_router(memory.router, prefix="/memory")

#in order to run it in the cli like "python -m main nightly-refresh" if the bool is true then add "--now" Note: we are using - not _, also we used main instead of main.py in order to be able to import a file from the same directory whithout issues
@typer_app.command()
def nightly_refresh(now : bool = False):
    if (now) : 
        ingest_files()
    else: 
        print('Scheduled Refresh')

@typer_app.command()
def create_tables_in_db():
    create_tables()


if __name__ == "__main__":
    typer_app()

    