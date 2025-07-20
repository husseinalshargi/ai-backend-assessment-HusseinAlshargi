import os
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import Annotated
from datetime import datetime


#save it in training_data (ensure it exsist)
upload_folder = "training_data"
os.makedirs(upload_folder, exist_ok=True)

train_router = APIRouter()

@train_router.post("/training/accept")
async def accept_training_document(
    file: Annotated[UploadFile, File(...)],
    tenant: Annotated[str, Form(...)]
):
    allowed_extensions = {".txt", ".json"}
    filename = file.filename.lower()

    #validate file extension to accept only txt/json files
    if not any(filename.endswith(ext) for ext in allowed_extensions):
        raise HTTPException(status_code=400, detail="Only .txt and .json files are allowed")
    
    #create a unique filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_filename = f"{tenant}_{timestamp}_{filename}"

    file_path = os.path.join(upload_folder, safe_filename)

    # Save the file to training_data/
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)

    return {"message": "File saved successfully", "filename": safe_filename}