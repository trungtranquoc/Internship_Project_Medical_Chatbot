from .state import State
from .base_node import BaseNode

class VietnameseTranslationNode(BaseNode):
    """
    Node for translating questions from Vietnamese to English.
    This node uses a translation model to convert the input question.
    """
    def _call(self, question: str):
        self._add_msg(("system", self._get_prompt("vietnamese_translation_system_prompt")))
        self._add_msg(("user", question))

        response = self._invoke()
        translated_question = response.strip()
        self.logger.info(f"Translated user query to: {translated_question}")

        return {
            'question': translated_question,
        }