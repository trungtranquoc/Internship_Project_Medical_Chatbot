from FlagEmbedding import FlagReranker
import numpy as np

class Reranker:
    def __init__(self, model_name: str, device: str = "cpu"):
        self.model = FlagReranker(model_name, devices=[device])

    def rerank(self, query: str, chunks: list[str]):
        pairs_query_chunk = [(query, chunk) for chunk in chunks]

        return self.model.compute_score(pairs_query_chunk, normalize=True)

    def top_k(self, query: str, chunks: list[str], k: int = 5):
        scores = self.rerank(query, chunks)
        top_k_indices = np.argsort(scores)[::-1][:k]

        return [chunks[i] for i in top_k_indices]

    def top_k_indices(self, query: str, chunks: list[str], k: int = 5):
        scores = self.rerank(query, chunks)
        top_k_indices = np.argsort(scores)[::-1][:k]

        return top_k_indices