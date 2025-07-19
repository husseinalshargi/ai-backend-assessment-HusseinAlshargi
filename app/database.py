#we used sqlalchemy rather than psycopg2 directly to handle the db connection and queries, as it is more powerful and easier to use
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from dotenv import load_dotenv
import os

load_dotenv()  #load environment variables from .env file

host=os.getenv("PostgreSQL_host")
password=os.getenv("PostgreSQL_password")
username = os.getenv("PostgreSQL_username")
dbname=os.getenv("PostgreSQL_dbname")
port=os.getenv("PostgreSQL_port")

print(f"Connecting to database at {host}:{port} with user {username} and database {dbname}")
#to connect to the db using sqlalchemy we need to create an engine
database_url = f"postgresql://{username}:{password}@{host}:{port}/{dbname}"
#after creating the url now we can create the engine, pool_pre_ping  -> in order to not connect to the db every time we execute a query, it will check if the connection is alive before executing
engine = create_engine(database_url, pool_pre_ping =True) 

#to create a session factory which will be used to create sessions when we need to interact with the db
#in order ro interact with the db we need to create a session to execute queries, flush -> convert to sql commands and execute them, commit -> save the changes to the db
sessionlocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

Base = declarative_base()





