import typer

from app.schemas.create_db_tables import create_tables
from app.services.evaluation import evaluate_answer
from app.services.ingestion import ingest_files


app = typer.Typer()


@app.command()
def nightly_refresh(now : bool = False):
    if (now) : 
        ingest_files()

@app.command()
def create_tables_in_db():
    create_tables()

@app.command()
def evaluate():
    evaluate_answer()
    


if __name__ == "__main__":
    app()
