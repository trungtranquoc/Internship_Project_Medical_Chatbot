from .VectorDB import VectorDB, NotFoundCollectionError
from ..models import EmbeddingModel
from pymilvus import connections, Collection
from pymilvus.exceptions import SchemaNotReadyException
from tqdm import tqdm
from functools import reduce

class MilvusDB(VectorDB):
    def __init__(self, embedding_model: EmbeddingModel, host: str, port: str):
        super().__init__(embedding_model)
        self.con = connections.connect(
            alias="default",
            host=host,
            port=port
        )

    def load_collection(self, collection_name: str):
        try:
            collection = Collection(collection_name)
            collection.load()
        except SchemaNotReadyException:
            raise NotFoundCollectionError(collection_name)

    def get_collection(self, collection_name: str) -> Collection:
        try:
            collection = Collection(collection_name)
            collection.load()

            return collection
        except SchemaNotReadyException:
            raise NotFoundCollectionError(collection_name)
        
    def create_collection(self, collection_name: str, schema):
        pass

    def query(self, collection_name: str, query: str, n_results: int = 3):
        collection = self.get_collection(collection_name)
        query_embedding = self.embedding_model.embed_text([query])

        data = collection.search(
            data=query_embedding,
            anns_field="embedding_vector",
            limit=n_results,
            param={"metric_type": "COSINE"},
            output_fields=["topic", "question", "answer"],
            consistency_level="Strong"
        )

        return data