from sqlalchemy import Column, Integer, String, Text, ForeignKey
from app.database import Base
from sqlalchemy.orm import relationship


#in order to create a model we need to create a class that inheret base class 
class DocumentChunkRecord(Base):
    __tablename__ = 'document_chuncks'

    id = Column(Integer, primary_key=True, index=True)  #primary key
    document_id = Column(Integer, ForeignKey("ingested_files.id"))  #unique identifier for the document
    chunk_text = Column(Text)  #the text of the chunk
    embedding = Column(Text)  #the embedding of the chunk, stored as a vector
    document = relationship("IngestedFileRecord", back_populates="chunks")

