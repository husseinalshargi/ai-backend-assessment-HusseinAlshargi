# a library that run cli commands which run tasks from the terminal without needing the user to write all the code 
import typer

from app.services.create_db_tables import create_tables
from app.services.ingestion import ingest_files

app = typer.Typer()

#in order to run it in the cli like "python -m main nightly-refresh" if the bool is true then add "--now" Note: we are using - not _, also we used main instead of main.py in order to be able to import a file from the same directory whithout issues
@app.command()
def nightly_refresh(now : bool = False):
    if (now) : 
        ingest_files()
    else: 
        print('Scheduled Refresh')

@app.command()
def create_tables_in_db():
    create_tables()


if __name__ == "__main__":
    app()

    