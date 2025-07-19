import os #to read files and env variables
import json #to read json files
import hashlib #to hash files
from pathlib import Path
from datetime import datetime #to handle dates and times

#as all the training files is in one place 
training_data_dir = "training_data/"

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
            print(f" file name: {file_name} - Hash: {file_hash[:16]} - Tokens: {tokens_estimate} - Last Modified: {datetime.fromtimestamp(Path(file_path).stat().st_mtime)}")
