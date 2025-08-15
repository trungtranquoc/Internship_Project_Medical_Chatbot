from typing import Annotated
from typing_extensions import TypedDict
import operator

class State(TypedDict):
    history: list[str]
    user_language: str           # Support for multilingual chatbot
    question: str
    context: list[dict]            # List of context documents
    answer: str                   # Generated answer
    question_type: str     # Type of question (e.g., general, medical, etc.)
    is_streaming: bool = False  # Flag for streaming mode