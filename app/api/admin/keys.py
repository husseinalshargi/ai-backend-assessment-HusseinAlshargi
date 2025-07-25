# app/routes/admin_keys.py
from fastapi import APIRouter,Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr


import app.database as db 
from app.models.api_keys_record import APIKey

class KeyCreateRequest(BaseModel):
    role: str
    owner_email: EmailStr




keys_router = APIRouter()

def get_db(): #make it here so we do not use the global one
    db_session = db.sessionlocal()
    try:
        yield db_session
    finally:
        db_session.close()


@keys_router.get("/get_keys")
def list_keys(db: Session = Depends(get_db)):
    return db.query(APIKey).all()

@keys_router.post("/create_key")
def create_key(payload: KeyCreateRequest, db: Session = Depends(get_db)):
    new_key = APIKey(
        role=payload.role,
        owner_email=payload.owner_email,
    )
    db.add(new_key)
    db.commit()
    db.refresh(new_key)
    return {"api_key": new_key.key}

@keys_router.post("/{key}/deactivate")
def deactivate_key(key: str, db: Session = Depends(get_db)):
    api_key = db.query(APIKey).filter_by(key=key).first()
    if not api_key:
        return JSONResponse(status_code=404, content={"detail":"API key not found"})
    api_key.active = False
    db.commit()
    return {"message": "Key deactivated"}

@keys_router.post("/{key}/activate")
def activate_key(key: str, db: Session = Depends(get_db)):
    api_key = db.query(APIKey).filter_by(key=key).first()
    if not api_key:
        return JSONResponse(status_code=404, content={"detail":"API key not found"})
    api_key.active = True
    db.commit()
    return {"message": "Key activated"}
