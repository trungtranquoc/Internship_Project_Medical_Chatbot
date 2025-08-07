from .VectorDB import VectorDB, NotFoundCollectionError
from pymilvus import connections, Collection
from pymilvus.exceptions import SchemaNotReadyException

from langchain_openai import OpenAIEmbeddings

import os

EMBEDDING_MODEL = os.environ.get("EMBEDDING_MODEL", "text-embedding-3-small")  # Default embedding model
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

class MilvusDB(VectorDB):
    def __init__(self, collection_name: str, host: str, port: str):
        super().__init__()
        self.con = connections.connect(
            alias="default",
            host=host,
            port=port
        )
        self.embedding_model = OpenAIEmbeddings(
            model=EMBEDDING_MODEL,
            api_key=os.environ.get("OPENAI_API_KEY")
        )
        self.collection = self.get_collection(collection_name)

    def get_collection(self, collection_name: str) -> Collection:
        try:
            collection = Collection(collection_name)
            collection.load()

            return collection
        except SchemaNotReadyException:
            raise NotFoundCollectionError(collection_name)
        
    def create_collection(self, text_chunks, collection_name):
        pass        # This method is not implemented in the original code

    def query(self, query: str, n_results: int = 3):
        query_embedding = self.embedding_model.embed_documents([query])

        data = self.collection.search(
            data=query_embedding,
            anns_field="embedding_vector",
            limit=n_results,
            param={"metric_type": "COSINE"},
            output_fields=["topic", "question", "answer", "keyword"],
            consistency_level="Strong"
        )

        return data