from pydantic import BaseModel

class ChatHistorySchema(BaseModel):
    """Model representing a chat history entry in the database."""
    thread_id: str
    question: str
    answer: str
    timestamp: str  # ISO format string for date and time