# a library that run cli commands which run tasks from the terminal without needing the user to write all the code 
import typer

from app.services.ingestion import ingest_files

app = typer.Typer()

#in order to run it in the cli like "python -m scripts.manage nightly-refresh" if the bool is true then add "--now" Note: we are using - not _, also we used scripts.manage instead of scripts/manage.py in order to be able to import a file from the same directory whithout issues
@app.command()
def nightly_refresh(now : bool = False):
    if (now) : 
        ingest_files()
    else: 
        print('Scheduled Refresh')

@app.command()
def nightly_refresh2(now : bool = False):
    #as there is a bug in in typer that don't work with only one command
    pass


if __name__ == "__main__":
    app()