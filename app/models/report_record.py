from sqlalchemy import Column, String, DateTime, func
from datetime import datetime
from app.database import Base


class GeneratedReport(Base):
    __tablename__ = "generated_reports"

    id = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=False)
    tenant = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
