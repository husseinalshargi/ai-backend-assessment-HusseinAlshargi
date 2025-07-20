from fastapi.responses import FileResponse
from fastapi import APIRouter, HTTPException
import app.database as db
from uuid import uuid4
import os
from pydantic import BaseModel
from typing import List

from app.services.generate_report import generate_docx_report
from app.models.report_record import GeneratedReport



#better to use pydantic in request models
class ReportRequest(BaseModel):
    title: str
    sections: List[str]
    prompt_context: str
    tenant: str

# http://localhost:8000/

generate_router = APIRouter()
session = db.session



@generate_router.post("/generate")
def generate_report(report : ReportRequest): #of type ReportRequest (also a table in the postsql db)
    try:
        file_id = str(uuid4()) #generate a random string id -> about 32 char length - excluded
        file_path = generate_docx_report(
            title=report.title,
            sections=report.sections,
            prompt_context=report.prompt_context,
            tenant=report.tenant,
            file_id=file_id
        )

        file_title = report.title
        return {
            "message": "Report generated successfully.",
            "report_id": file_id,
            "report_title": file_title,
            "download_url": f"/api/report/{file_id}/{file_title}/download"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@generate_router.get("/{report_id}/{file_title}/download")
def download_report(report_id, file_title):
    file_path = f"generated_reports/{report_id}.docx"
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Report not found")
    return FileResponse(file_path, media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document', filename=f"{file_title + "-" + report_id}.docx") #to expose the endpoint for downloading
