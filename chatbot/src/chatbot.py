import os

from .vector_database import MilvusDB
from .utils import generate_RAG_prompt, system_prompt, Metadata
from .models import EmbeddingModel, CausalModel, Reranker
import time

import dotenv
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(stream_handler)

# Load env file
env = os.getenv("ENV", "development")
dotenv.load_dotenv(f".env.{env}", override=True)

OPEN_API_KEY = os.environ.get("OPENAI_API_KEY")                   # Use for embedding vector
EMBEDDING_MODEL = os.environ.get("EMBEDDING_MODEL", "text-embedding-3-small")  # Default embedding model
CAUSAL_MODEL = os.environ.get("CAUSAL_MODEL", "gpt-4o-mini")      # Default causal model
RERANKER_MODEL = os.environ.get("RERANKER_MODEL", "BAAI/bge-reranker-v2-m3")  # Default reranker model
MILVUS_HOST = os.environ.get("MILVUS_HOST", "localhost")  # Default Milvus host
MILVUS_PORT = int(os.environ.get("MILVUS_PORT", 19530))
COLLECTION_NAME = os.environ.get("COLLECTION_NAME", "medical_QA_embedding")  # Default collection name

DEVICE = os.environ.get("DEVICE", "cpu")  # Default device for reranker

if not OPEN_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in .env file")

class Chatbot:
    def __init__(self, device: str = DEVICE):
        self.device = device
        self.collection_name = COLLECTION_NAME

    def start(self):

        # Step 1: Loading model
        logger.info(f"Prepare Chatbot in device {self.device}. Loading LLM models: Causual, Embedding, Reranker...")
        self.causal_model = CausalModel(model_name=CAUSAL_MODEL, api_key=OPEN_API_KEY, system_prompt=system_prompt)
        self.embedding_model = EmbeddingModel(model_name=EMBEDDING_MODEL, api_key=OPEN_API_KEY)
        self.reranker = Reranker(model_name=RERANKER_MODEL, device=self.device)

        # Step 3: Loading chromadb database
        logger.info("Loading milvus database...")
        self.vector_db = MilvusDB(embedding_model=self.embedding_model, host=MILVUS_HOST, port=MILVUS_PORT)
        self.vector_db.load_collection(self.collection_name)
        logger.info("Milvus database loaded successfully")

    def answer(self, question: str, history: list[str] = []) -> tuple[str, list[str]]:
        logger.info("🤖 Answering...")
        chunks_data = self.vector_db.query(self.collection_name, query=question, n_results=20)

        # Data: text and metadata
        chunks_data = [chunk['entity'] for chunk in chunks_data[0]]
        docs = [chunk['answer'] for chunk in chunks_data]

        # Classify question type
        question_type = self.causal_model.classify_question(question)
        logger.info(f"Classified question type: {question_type}")

        # Reranking docs and get unique indices
        start = time.time()
        
        rerank_idx = self.reranker.top_k_indices(question, docs, k=3)
        top_docs = [docs[idx] for idx in rerank_idx]
        related_questions = [chunks_data[idx]['question'] for idx in rerank_idx]

        logger.info(f"Reranking time: {time.time() - start:.2f} seconds. Related questions found: {related_questions}")

        # Generate prompt and answer
        prompt = generate_RAG_prompt(question, top_docs=top_docs, question_type_enum=question_type)
        answer = self.causal_model.generate_response(prompt, history=history)
        
        # return generate_answer_with_source(answer, source), source
        return answer, related_questions