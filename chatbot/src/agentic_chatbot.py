import dotenv
import os
from typing import Union, Generator, AsyncGenerator

dotenv.load_dotenv('../.env.development', override=True)

from .nodes import QuestionClassificationNode, AnswerGenerationNode, RAGRetrieveNode, QueryRewriteNode, State, DetectLanguageNode, VietnameseTranslationNode, GraphNodeException
from .langfuse_config import langfuse_callback
from langgraph.graph import StateGraph, START, END
from .logger import CustomLogger
from nguyenpanda.swan import blue_violet, aqua, green_yellow, light_coral, blue, light_pink, misty_rose

LANGFUSE_AVAILABLE = os.getenv("LANGFUSE_AVAILABLE", "False") != "False"

class AgenticChatbot(StateGraph):
    def __init__(self):
        self.graph_builder = StateGraph(State)
        self.graph = None
        self.logger = CustomLogger('agentic_chatbot', misty_rose)

    def start(self):
        self.graph_builder.add_node("query_rewrite", QueryRewriteNode(CustomLogger('query_rewrite', light_coral)))
        self.graph_builder.add_node("question_classification", QuestionClassificationNode(CustomLogger('question_classification', aqua)))
        self.graph_builder.add_node("rag_retrieve", RAGRetrieveNode(CustomLogger('rag_retrieve', blue_violet)))
        self.graph_builder.add_node("answer_generation", AnswerGenerationNode(CustomLogger('answer_generation', green_yellow)))
        self.graph_builder.add_node("language_detection", DetectLanguageNode(CustomLogger('language_detection', light_pink)))
        self.graph_builder.add_node("vietnamese_translation", VietnameseTranslationNode(CustomLogger('vietnamese_translation', blue)))

        self.graph_builder.add_edge(START, "language_detection")
        self.graph_builder.add_conditional_edges(
            "language_detection",
            lambda state: state['user_language'],
            {
                "english": "query_rewrite",
                "vietnamese": "vietnamese_translation",
                "unsupported": END
            }
        )

        self.graph_builder.add_edge("vietnamese_translation", "query_rewrite")
        self.graph_builder.add_edge("query_rewrite", "question_classification")
        self.graph_builder.add_edge("query_rewrite", "rag_retrieve")
        self.graph_builder.add_edge("question_classification", "answer_generation")
        self.graph_builder.add_edge("rag_retrieve", "answer_generation")
        self.graph_builder.add_edge("answer_generation", END)

        if LANGFUSE_AVAILABLE:
            self.graph = self.graph_builder.compile().with_config({"callbacks": [langfuse_callback]})
        else:
            # Not use Langfuse for observability
            self.graph = self.graph_builder.compile()

    def answer(self, question: str, history: list = []) -> str:
        """
        Process a question and return the classified question type, keywords, and related questions.
        """
        self.logger.info(f"Processing question: {question}")

        state = State({
            'question': question,
            'history': [
                {
                    'role': item.role,
                    'content': item.content
                }  for item in history],
            "answer": "",
            "context": [],
            "question_type": "",
            "user_language": "english"
        })

        state = self.graph.run(state)
        return state['answer']

    async def start_streaming(self, question: str, history: list = []) -> AsyncGenerator[str, None]:
        """
        Start streaming answers for a given question with the provided history.
        This method is used for gRPC streaming responses.
        """
        self.logger.info(f"Processing question: {question}")

        state = State({
            'question': question,
            'history': [
                {
                    'role': item.role,
                    'content': item.content
                }  for item in history],
            "answer": "",
            "context": [],
            "question_type": "",
            "user_language": "english",
            "is_streaming": True
        })
        
        async for event in self.graph.astream(state, stream_mode="messages"):
            if not event[1].get("langgraph_node", "").endswith("generation"):
                continue
            msg = event[0]
            yield msg.text()

        self.logger.info(f"Answer streaming completed for question: {question}")