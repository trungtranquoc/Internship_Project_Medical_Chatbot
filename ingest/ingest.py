import os
import pandas as pd
import kagglehub
from tqdm import tqdm
from time import sleep
from typing import List
from pymilvus import connections, utility, Collection, FieldSchema, DataType, CollectionSchema
from langchain_openai import OpenAIEmbeddings

# --- 1. CONFIGURATION ---
# These will be provided by Kubernetes ConfigMaps and Secrets
MILVUS_HOST = os.getenv("MILVUS_HOST")
MILVUS_PORT = int(os.getenv("MILVUS_PORT", 19530))
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
COLLECTION_NAME = os.getenv("MILVUS_COLLECTION")

MAX_TOKEN_BATCH = 20000
MILVUS_BATCH_SIZE = 1000
EMBEDDING_MODEL = "text-embedding-3-small"
    
# --- 2. DATA LOADING & PROCESSING ---
def prepare_data():
    print("🌍 Downloading dataset from Kaggle...")
    path = kagglehub.dataset_download("gvaldenebro/cancer-q-and-a-dataset")
    
    csv_files = []
    for root, _, files in os.walk(path):
        for file in files:
            if file.endswith(".csv"):
                csv_files.append(os.path.join(root, file))

    full_df = pd.concat([pd.read_csv(f) for f in csv_files], axis=0)
    full_df.drop_duplicates(subset=['Question', 'Answer'], inplace=True)
    
    # Calculate token approximate and format text
    full_df['count_word'] = full_df.apply(lambda x: len(str(x['Question']).split()) + len(str(x['Answer']).split()), axis=1)
    full_df['Text'] = "**Question**: " + full_df['Question'] + "\n\n **Answer:** " + full_df['Answer']
    # Add topic field if not present
    if 'topic' not in full_df.columns:
        full_df['topic'] = "Cancer Q&A"
    
    return full_df

class TextBatcher:
    def __init__(self, texts, counts):
        self.texts = texts
        self.counts = counts

    def get_batches(self):
        current_batch, current_count = [], 0
        for text, count in zip(self.texts, self.counts):
            if current_count + count > MAX_TOKEN_BATCH:
                yield current_batch
                current_batch, current_count = [], 0
            current_batch.append(text)
            current_count += count
        if current_batch:
            yield current_batch

# --- 3. MILVUS OPERATIONS ---
def setup_milvus_collection():
    connections.connect(alias="default", host=MILVUS_HOST, port=MILVUS_PORT)
    
    if utility.has_collection(COLLECTION_NAME):
        print(f"⚠️ Collection {COLLECTION_NAME} already exists. Skipping creation.")
        return Collection(COLLECTION_NAME)

    fields = [
        FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
        FieldSchema(name="embedding_vector", dtype=DataType.FLOAT_VECTOR, dim=1536),
        FieldSchema(name="question", dtype=DataType.VARCHAR, max_length=1000), # Increased for safety
        FieldSchema(name="answer", dtype=DataType.VARCHAR, max_length=30000),
        FieldSchema(name="topic", dtype=DataType.VARCHAR, max_length=500),
    ]
    
    schema = CollectionSchema(fields=fields, description="Medical Chatbot Vector Database")
    collection = Collection(name=COLLECTION_NAME, schema=schema)
    
    index_params = {
        "index_type": "IVF_FLAT",
        "metric_type": "COSINE",
        "params": {"nlist": 128},
    }
    collection.create_index(field_name="embedding_vector", index_params=index_params)
    return collection

# --- 4. MAIN EXECUTION ---
def main():
    if not OPENAI_API_KEY:
        raise ValueError("❌ OPENAI_API_KEY not found in environment variables!")

    df = prepare_data()
    collection = setup_milvus_collection()
    embedder = OpenAIEmbeddings(model=EMBEDDING_MODEL, api_key=OPENAI_API_KEY)

    # Batch Embedding
    batcher = TextBatcher(df['Text'].tolist(), df['count_word'].tolist())
    all_embeddings = []
    
    print("🧠 Generating embeddings...")
    batches = list(batcher.get_batches())
    for i, batch in enumerate(tqdm(batches)):
        if i > 0:
            sleep(65)  # Sleep between every batch to respect rate limits
        all_embeddings.extend(embedder.embed_documents(batch))

    # Data Insertion
    print("💾 Inserting data into Milvus...")
    insert_data = [
        {
            "embedding_vector": emb,
            "question": q,
            "answer": a,
            "topic": t,
        }
        for emb, q, a, t in zip(all_embeddings, df['Question'].tolist(), df['Answer'].tolist(), df['topic'].tolist())
    ]

    for i in range(0, len(insert_data), MILVUS_BATCH_SIZE):
        collection.insert(insert_data[i : i + MILVUS_BATCH_SIZE])
    
    collection.flush()
    print(f"✅ Successfully ingested {len(insert_data)} records into {COLLECTION_NAME}!")

if __name__ == "__main__":
    main()