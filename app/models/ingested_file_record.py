from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, func
from app.database import Base

#in order to create a model we need to create a class that inheret base class 
class IngestedFileRecord(Base):
    __tablename__ = 'ingested_files'

    id = Column(Integer, primary_key=True, autoincrement=True)
    file_name = Column(Text, unique=True, nullable=False)
    file_hash = Column(Text, nullable=False)
    token_estimate = Column(Integer, nullable=False)
    #timezone to store as timestamp in UTC and retrive in user's timezone
    #func_now() is used to set the default value of the column to the current timestamp
    process_date = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    tenant = Column(String(50), default='public')  # Default tenant is 'public'