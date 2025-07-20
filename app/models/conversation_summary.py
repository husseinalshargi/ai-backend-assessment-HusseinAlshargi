from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, func
from datetime import datetime
from app.database import Base

class ConversationSummary(Base):
    __tablename__ = "conversation_summaries"

    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(String, index=True)
    summary = Column(Text, nullable=False)
    turn_number = Column(Integer) # to track the turn number in the conversation
    timestamp = Column(DateTime(timezone=True), server_default=func.now())  # to store the timestamp of the summary creation
