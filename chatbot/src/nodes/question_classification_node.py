from ..utils import QuestionType
from .state import State
import os

from .base_node import BaseNode
from langchain_core.output_parsers import PydanticOutputParser

from pydantic import BaseModel, Field

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
model_name = os.environ.get("CAUSAL_MODEL", "gpt-4o-mini")

class QuestionDescription(BaseModel):
    question_type: QuestionType = Field(description="The classified type of the medical question")

class QuestionClassificationNode(BaseNode):
    def __init__(self, logger):
        super().__init__(logger)
        self.question_classifier = PydanticOutputParser(pydantic_object=QuestionDescription)

    def _call(self, question: str):
        self._add_msg(("user", self._get_prompt("question_classification_prompt").format(question=question) + f"\n\n{self.question_classifier.get_format_instructions()}"))

        try:
            response = self._invoke()
            question_description = self.question_classifier.parse(response)
            
            self.logger.info(f"Question classification: {question_description}")
            
            question_type = question_description.question_type
            
        except Exception as e:
            self.logger.error(f"Error in question classification: {e}")
            self.logger.error(f"Raw response: {response if 'response' in locals() else 'No response'}")
            
            # Fallback: try to extract question type directly from response
            if 'response' in locals():
                response_text = response.strip().upper()
                try:
                    # Try to match the response directly to QuestionType enum
                    question_type = QuestionType(response_text)
                    self.logger.info(f"Fallback classification successful: {question_type}")
                except ValueError:
                    # Ultimate fallback
                    self.logger.warning(f"Using ultimate fallback classification: EXPLANATION")
                    question_type = QuestionType.GENERAL_INFO
            else:
                # No response available, use default
                self.logger.warning(f"No response available, using fallback classification: EXPLANATION")
                question_type = QuestionType.GENERAL_INFO

        return {
            'question_type': question_type
        }