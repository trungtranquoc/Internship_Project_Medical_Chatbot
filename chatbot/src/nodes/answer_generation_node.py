from ..utils import QUESTION_DESCRIPTION
from .base_node import BaseNode
from .state import State
from .exception import InsufficientInformationError

class AnswerGenerationNode(BaseNode):
    """
    Node for generating answers based on medical questions and provided documents.
    This node uses a classification prompt to determine the type of question and
    generates an appropriate answer using the provided medical documents.
    """
    def _call(self, context: dict, question: str, question_type: str, user_language: str):
        if not context:
            raise InsufficientInformationError()
        context = '\n\n'.join([data['answer'] for data in context])

        # Get specific instructions based on question type
        type_info = QUESTION_DESCRIPTION.get(question_type, {})
        specific_instructions = type_info.get("instructions", "Provide a balanced response focusing on key information.")

        self._add_msg(("system", self._get_prompt("answer_generation_system_prompt")))
        self._add_msg(("user", self._get_prompt("answer_generation_user_prompt", user_language).format(
            user_question=question,
            doc=context,
            question_type=question_type.value if question_type else "general",
            specific_instructions=specific_instructions,
        )))

        response = self._invoke()

        self.logger.info(f"Generated answer completed !")

        return {
            'answer': response,
        }