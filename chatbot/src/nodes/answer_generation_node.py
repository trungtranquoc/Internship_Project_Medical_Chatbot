from typing import Union, AsyncGenerator
from langfuse import observe

from ..utils import QUESTION_DESCRIPTION
from .base_node import BaseNode
from .state import State
from .exception import InsufficientInformationError
from ..models import open_ai_model

class AnswerGenerationNode(BaseNode):
    """
    Node for generating answers based on medical questions and provided documents.
    This node uses a classification prompt to determine the type of question and
    generates an appropriate answer using the provided medical documents.
    """
    @observe(name="answer_generation_node", as_type="generation", transform_to_string=lambda x: " ".join(x))
    async def _chat(self, msgs: list) -> AsyncGenerator[str, None]:
        async for chunk in open_ai_model.astream(self.msgs):
            yield chunk.content

    # @observe("answer_generation_node") 
    async def __call__(self, state: State):
        question_type = state.get('question_type', None)
        question = state.get('question', "")
        user_language = state.get('user_language', "english")
        context = state.get('context', [])
        is_streaming = state.get('is_streaming', False)

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

        if is_streaming:
            self.logger.info(f"Generating answer for question: {question}.")
            full_msg = ""
            async for chunk in self._chat(self.msgs):
                full_msg += chunk + " "
                yield {"answer": chunk}
            yield {"answer": full_msg.strip()}
            self.logger.info(f"Generated answer completed !")
        else:
            response = self._invoke()
            yield {'answer': response}