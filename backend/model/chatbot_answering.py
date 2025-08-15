from pydantic import BaseModel
from typing import Optional

class ChatbotAnswering(BaseModel):
    answer: str
    time_to_first_token: Optional[float] = None
    inference_time: Optional[float] = None