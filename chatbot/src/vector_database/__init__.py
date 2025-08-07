from .ChromaDB import ChromaDB
from .MilvusDB import MilvusDB
from .VectorDB import VectorDB
from .VectorDB import NotFoundCollectionError

import os

MILVUS_HOST = os.environ.get("MILVUS_HOST", "localhost")  # Default Milvus host
MILVUS_PORT = int(os.environ.get("MILVUS_PORT", 19530))
COLLECTION_NAME = os.environ.get("MILVUS_COLLECTION", "medical_database_v3")  # Default collection name

db = MilvusDB(
    collection_name=COLLECTION_NAME,
    host=MILVUS_HOST,
    port=MILVUS_PORT
)

__all__ = ["ChromaDB", "MilvusDB", "VectorDB", "NotFoundCollectionError", "db"]