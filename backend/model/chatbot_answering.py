from pydantic import BaseModel

class ChatbotAnswering(BaseModel):
    answer: str
    related_questions: list[str]
    inference_time: float = None