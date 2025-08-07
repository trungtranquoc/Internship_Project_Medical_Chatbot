from langchain_openai import ChatOpenAI
import os

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
BASE_URL_API = os.environ.get("BASE_URL_API", None)  # None => Mount to Google Provider
MODEL_NAME = os.environ.get("CAUSAL_MODEL", "gpt-4o-mini")

open_ai_model = ChatOpenAI(
    api_key=OPENAI_API_KEY,
    base_url=BASE_URL_API or None,
    model=MODEL_NAME,
    temperature=0.2,
)