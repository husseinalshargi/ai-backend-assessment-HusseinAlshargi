from sqlalchemy_utils import database_exists, create_database

#in order to create tables we need the engine and a base of the models
from app.database import engine, Base
#not sure why yet..  but we need to import the model to create the table
from app.models.ingested_file_record import IngestedFileRecord


def create_tables():
    #ensure the database exists before creating tables
    if not database_exists(engine.url):
        create_database(engine.url)
        print(f"Database created at {engine.url}")
    # Create all tables in the database
    Base.metadata.create_all(bind = engine)
    print("Tables created successfully.")
