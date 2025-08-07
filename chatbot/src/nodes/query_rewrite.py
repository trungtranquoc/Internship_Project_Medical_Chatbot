import os

from .state import State
from .base_node import BaseNode

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
MODEL_NAME = os.environ.get("CAUSAL_MODEL", "gpt-4o-mini")

class QueryRewriteNode(BaseNode):
    """
    Node for rewriting the current question based on conversation history into standalone query.
    """

    def _call(self, question: str, history: list, user_language: str) -> State:
        """Rewrite the current question using conversation history"""
        self.logger.info("Starting query rewriting...")
        
        # Skip rewriting if no history or history is empty
        try:
            self._add_msg(("system", self._get_prompt("query_rewrite_system_prompt")))
            # History
            [self._add_msg((msg['role'], msg['content'])) for msg in history]
            self._add_msg(("user", self._get_prompt("query_rewrite_user_prompt").format(current_question=question)))
            
            # Get rewritten query
            response = self._invoke()
            rewritten_query = response.strip()
            
            # Log the rewriting result
            if rewritten_query != question:
                self.logger.info(f"Query rewritten from: '{question}' to: '{rewritten_query}'")
            else:
                self.logger.info("Query unchanged after rewriting process")
            
            # Update state with rewritten query
            return {
                'question': rewritten_query,
            }
            
        except Exception as e:
            self.logger.error(f"Error in query rewriting: {e}")
            return {}