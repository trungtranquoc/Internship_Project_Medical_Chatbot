from .state import State
from FlagEmbedding import FlagReranker
import os
import numpy as np
from time import time

from ..vector_database import db
from .base_node import BaseNode

RAG_SEARCH_LIMIT = 5  # Limit for RAG search results
CONTEXT_LIMIT = 3  # Limit for context documents

# Turn off warnings from transformers
os.environ['TRANSFORMERS_NO_ADVISORY_WARNINGS'] = 'true'
RERANKER_MODEL = os.environ.get("RERANKER_MODEL", "BAAI/bge-reranker-v2-m3")  # Default reranker model
DEVICE = os.environ.get("DEVICE", "cpu")  # Default device for reranker

class RAGRetrieveNode(BaseNode):
    def __init__(self, logger):
        super().__init__(logger)
        self.database = db
        self.reranker_model = FlagReranker(RERANKER_MODEL, devices=DEVICE)

    def _semantic_search(self, question: str) -> list:
        chunks_data = self.database.query(query=question, n_results=RAG_SEARCH_LIMIT)

        # Data: text and metadata
        chunks_data = [chunk['entity'] for chunk in chunks_data[0]]
        # docs = [chunk['answer'] for chunk in chunks_data]
        return chunks_data

    def _reranking(self, question: str, docs: list[str]) -> list[int]:
        pairs_query_chunk = [(question, chunk) for chunk in docs]
        scores = self.reranker_model.compute_score(pairs_query_chunk, normalize=True)

        # Return indices
        return np.argsort(scores)[::-1][:CONTEXT_LIMIT]
    
    def _call(self, question: str):
        start = time()
        chunks_data = self._semantic_search(question)

        top_docs_idx = self._reranking(question, [chunk['answer'] for chunk in chunks_data])
        self.logger.info("Reranker time: {:.2f} seconds. Related medical status: {}".format(time() - start, list(set([chunks_data[idx]['keyword'] for idx in top_docs_idx]))))

        return {
            'context': [chunks_data[idx] for idx in top_docs_idx]
        }