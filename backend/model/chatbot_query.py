from pydantic import BaseModel

class ChatbotQuery(BaseModel):
    question: str
    thread_id: str