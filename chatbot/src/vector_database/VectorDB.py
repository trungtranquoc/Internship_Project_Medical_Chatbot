from abc import ABC, abstractmethod
from ..models import EmbeddingModel

class NotFoundCollectionError(Exception):
    def __init__(self, collection_name: str):
        super().__init__(f"Collection {collection_name} not found")

class VectorDB(ABC):
    def __init__(self, embedding_model: EmbeddingModel):
        self.embedding_model = embedding_model

    @abstractmethod
    def get_collection(self, collection_name: str):
        pass

    @abstractmethod
    def create_collection(self, text_chunks: list[str], collection_name: str):
        pass

    @abstractmethod
    def query(self, collection_name: str, query: str, n_results: int = 3):
        pass