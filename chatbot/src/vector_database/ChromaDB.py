import chromadb
import os
from tqdm import tqdm
from ..models import EmbeddingModel
from .VectorDB import NotFoundCollectionError, VectorDB

CLIENT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data/chromadb'))

class ChromaDB(VectorDB):
    def __init__(self, embedding_model: EmbeddingModel, client_path = CLIENT_PATH):
        self.client = chromadb.PersistentClient(path=client_path)
        self.embedding_model = embedding_model
        
    def get_collection(self, collection_name: str):
        try:
            return self.client.get_collection(collection_name)
        except Exception as e:
            raise NotFoundCollectionError(collection_name)

    def create_collection(self, text_chunks: list[str], collection_name):
        chunk_embeddings = [self.embedding_model.embed_text(chunk) for chunk in tqdm(text_chunks, desc="Vectorizing text chunks")]

        collection = self.client.create_collection(name=collection_name)
        # 5. Add manually-embedded documents
        for i, (chunk, embedding) in tqdm(enumerate(zip(text_chunks, chunk_embeddings)), desc="Adding documents to collection", total=len(text_chunks)):
            collection.add(
                documents=[chunk],
                ids=[str(i)],
                embeddings=[embedding],
                metadatas=[{"source": "doc"}]           
            )
            
        return collection

    def query(self, collection_name: str, query: str, n_results: int = 3):
        collection = self.get_collection(collection_name)
        query_embedding = self.embedding_model.embed_text(query)
        
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )
        return results