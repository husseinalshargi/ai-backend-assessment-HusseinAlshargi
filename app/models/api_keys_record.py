from sqlalchemy import Boolean, Column, Integer, String, Text, DateTime, ForeignKey, func
from app.database import Base
import uuid #in order to create an api key

class APIKey(Base):
    __tablename__ = "api_keys"

    key = Column(String, primary_key=True, index= True, default= lambda: str(uuid.uuid4()))
    role = Column(String, nullable= False)
    owner_email = Column(String, nullable= False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_used_at = Column(DateTime, nullable=True)
    active = Column(Boolean, default= True)