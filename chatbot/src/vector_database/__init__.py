from .ChromaDB import ChromaDB
from .MilvusDB import MilvusDB
from .VectorDB import VectorDB
from .VectorDB import NotFoundCollectionError

import os

MILVUS_HOST = os.environ.get("MILVUS_HOST")  # Default Milvus host
MILVUS_PORT = int(os.environ.get("MILVUS_PORT"))  # Default Milvus port
COLLECTION_NAME = os.environ.get("MILVUS_COLLECTION")  # Default collection name

db = MilvusDB(
    collection_name=COLLECTION_NAME,
    host=MILVUS_HOST,
    port=MILVUS_PORT
)

__all__ = ["ChromaDB", "MilvusDB", "VectorDB", "NotFoundCollectionError", "db"]