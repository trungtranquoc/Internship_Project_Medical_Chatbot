from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel
from typing import Literal

from .state import State
from .exception import LanguageDetectionError
from .base_node import BaseNode

class LanguageDetectionOutput(BaseModel):
    language: Literal["vietnamese", "english", "unsupported"]

class DetectLanguageNode(BaseNode):
    """
    Node for detecting the language of the input question.
    This node uses a language detection model to determine if the question is in Vietnamese.
    """
    def __init__(self, logger):
        super().__init__(logger)
        self.output_parser = PydanticOutputParser(pydantic_object=LanguageDetectionOutput)

    def _call(self, question: str):
        self._add_msg(("user", self._get_prompt("language_detection_prompt").format(question=question) + f"\n\n{self.output_parser.get_format_instructions()}"))
        response = self._invoke()

        detected_language = self.output_parser.parse(response).language
        if detected_language == "unsupported":
            raise LanguageDetectionError()
        self.logger.info(f"Detected language: {detected_language}")

        return {
            "user_language": detected_language,
        }
