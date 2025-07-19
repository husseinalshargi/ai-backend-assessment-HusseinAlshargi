import os #to read files and env variables
import json #to read json files
import hashlib #to hash files
from pathlib import Path
from datetime import datetime #to handle dates and times
from app.database import sessionlocal #to create a session to interact with the db
from app.models.ingested_file_record import IngestedFileRecord #to use the model to create a record in the db

session = sessionlocal() #create a session to interact with the db

#as all the training files is in one place 
training_data_dir = "training_data/"

# as the files could be large we need to chunk them to avoid performance issues when processing them using LLM, the overlapping is used to ensure that the chunks are not too small and to avoid losing context
def chunk_text(text, chunk_size=500, overlap=50):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap  #move start forward by chunk_size - overlap to also include some of the previous chunk in the next one
    return chunks #return a list of chunks


#to ensure file isn't processed multiple times
def is_file_processed(file_hash):
    #first to retrieve the record from the db to check if it exists
    return session.query(IngestedFileRecord).filter_by(file_hash=file_hash).first() is not None


#reads a text file and returns its content
def load_text_file(file_path):
    #check if the text file is empty
    if os.stat(file_path).st_size == 0:
        return ""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

#reads a json file and returns its content
def load_json_File(file_path):
    if os.stat(file_path).st_size == 0:
        return "{}"
    with open(file_path, 'r', encoding='utf-8') as file:
        #check if the file is empty
        data = json.load(file)
        #check the data type to ensure json format, return as json format string (indent to be more readable when printed)
        if isinstance(data, dict):
            return json.dumps(data, indent=2)
        if isinstance(data, list):
            #if the json file converted to a list of dicts then join them with new line after converting each dict to json format string 
            return "\n".join(json.dumps(item, indent=2) for item in data)
        else:
            #if it was null or any other type, return it as a string
            return str(data)

#hash is important to check if the file is changed or not also to handle large files whithout affecting performance
def hash_file(content):
    #sha256 is the most common hashing algorithm, hexdigest is used to return the hash in hexadecimal format as it is easier to read and store, encode is used to convert the string to bytes as the hashing algorithm works on bytes
    return hashlib.sha256(content.encode('utf-8')).hexdigest()

def save_record(file_name, file_hash, tokens_estimate, tenant='public'):
#check if the file is already processed to avoid duplicates
    if not is_file_processed(file_hash):   
        #create a new record in the db
        record = IngestedFileRecord(
                file_name=file_name,
                file_hash=file_hash,
                token_estimate=tokens_estimate,
                tenant=tenant  
        )
        #add the record to the session
        session.add(record)
        #flush the session to ensure the record is added to the db
        session.flush()
        #commit the session to save the changes to the db
        session.commit()

        return True
    else:
        print(f"File {file_name} is already processed, skipping.")
        return False

#now the ingestion function
def ingest_files():
    #list all files in the training data directory
    files = os.listdir(training_data_dir)
    #folder could have inside it files and folders, we include all files inside the folder and subfolders
    #os.walk is used to iterate over all files and folders in the directory
    for dir_path, _, file_names in os.walk(training_data_dir):
        for file_name in file_names:
            file_path = os.path.join(Path(dir_path), file_name)
            #get the file extension
            file_extension = Path(file_name).suffix.lower()

            #only accept text and json files
            if file_extension == '.txt':
                content = load_text_file(file_path)
            elif file_extension == '.json':
                content = load_json_File(file_path)
            else:
                print(f"Skipping file: {file_name}, which has type of {file_extension}")
                continue
            #now hash the content of the file
            file_hash = hash_file(content)
            #estimate tokens by counting words
            tokens_estimate = len(content.split())  
            
            #file_path.stat is used to get the file metadata, st_mtime is the last modified time of the file and lastly datetime.fromtimestamp is used to convert the timestamp to a readable format
            #print(f" file name: {file_name} - Hash: {file_hash[:16]} - Tokens: {tokens_estimate} - Last Modified: {datetime.fromtimestamp(Path(file_path).stat().st_mtime)}")

            #save the record in the db
            isSaved = save_record(file_name, file_hash, tokens_estimate, tenant='public')

            if not isSaved:
                continue

            #chunk the content to avoid performance issues when processing large files
            chunks = chunk_text(content)
            
