import chromadb
import os
from tqdm import tqdm
from langchain_openai import OpenAIEmbeddings
from .VectorDB import NotFoundCollectionError, VectorDB

CLIENT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data/chromadb'))
EMBEDDING_MODEL = os.environ.get("EMBEDDING_MODEL", "text-embedding-3-small")

class ChromaDB(VectorDB):
    def __init__(self, collection_name: str, client_path = CLIENT_PATH):
        self.client = chromadb.PersistentClient(path=client_path)
        self.embedding_model = OpenAIEmbeddings(
            model=EMBEDDING_MODEL,
            api_key=os.environ.get("OPENAI_API_KEY")
        )
        self.collection = self.get_collection(collection_name)
        
    def get_collection(self, collection_name: str):
        try:
            return self.client.get_collection(collection_name)
        except Exception as e:
            raise NotFoundCollectionError(collection_name)

    def create_collection(self, text_chunks: list[str], collection_name):
        chunk_embeddings = [self.embedding_model.embed_documents(chunk) for chunk in tqdm(text_chunks, desc="Vectorizing text chunks")]

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

    def query(self, query: str, n_results: int = 3):
        query_embedding = self.embedding_model.embed_text(query)

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )
        return results