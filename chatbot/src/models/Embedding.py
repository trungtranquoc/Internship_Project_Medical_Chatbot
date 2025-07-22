# from openai import OpenAI, RateLimitError
from langchain_openai import OpenAIEmbeddings
from langchain_core.embeddings import Embeddings
from langchain_openai.embeddings import OpenAIEmbeddings

class EmbeddingModel:
    def __init__(self, model_name: str, api_key):
        self.model_name = model_name
        self.api_key = api_key
        self.client = OpenAIEmbeddings(model=self.model_name, api_key=self.api_key)

    def embed_text(self, texts: list[str]):
        response = self.client.embed_documents(texts)

        return response
    
    def get_embedding(self) -> Embeddings:
        return OpenAIEmbeddings(model=self.model_name, api_key=self.api_key)