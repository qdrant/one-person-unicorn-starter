#!/usr/bin/env python
import os
import time

from datasets import load_dataset
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import CollectionStatus, Document, PointStruct, VectorParams

load_dotenv()

# --- Config ----------------------------------------------------

QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
QDRANT_URL = os.getenv("QDRANT_URL")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")
VECTOR_SIZE = os.getenv("VECTOR_SIZE")
DISTANCE_METRIC = os.getenv("DISTANCE_METRIC")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")

DATASET_NAME = "SnehaDeshmukh/IndianBailJudgments-1200"
BATCH_SIZE = 64
UPLOAD_PARALLEL = 16
VECTOR_NAME = f"fast-{EMBEDDING_MODEL.split("/")[-1].lower()}"


if __name__ == "__main__":
    # --- 1. Initialize Qdrant Client ---
    qdrant_client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY, prefer_grpc=True, timeout=30)

    # --- 2. Recreate Collection ---
    if qdrant_client.collection_exists(collection_name=COLLECTION_NAME):
        qdrant_client.delete_collection(collection_name=COLLECTION_NAME)
    vectors_config = {VECTOR_NAME: VectorParams(size=VECTOR_SIZE, distance=DISTANCE_METRIC)}
    qdrant_client.create_collection(collection_name=COLLECTION_NAME, vectors_config=vectors_config)

    # --- 3. Build Points ---
    dataset = load_dataset(DATASET_NAME, split="train")
    points = [PointStruct(id=i, payload={"document": dataset[i]["case_title"] + ": " + dataset[i].get("summary", ""), "metadata": dataset[i]}, vector={VECTOR_NAME: Document(text=dataset[i]["summary"], model=EMBEDDING_MODEL)}) for i in range(len(dataset))]

    # --- 4. Upload Points ---
    qdrant_client.upload_points(COLLECTION_NAME, points, batch_size=BATCH_SIZE, parallel=UPLOAD_PARALLEL)

    # --- 5. Wait for Collection to be Ready ---
    while qdrant_client.get_collection(COLLECTION_NAME).status != CollectionStatus.GREEN:
        time.sleep(1.0)

    # --- 6. Sanity Check: Query the first point ---
    query_text = dataset[0]["case_title"] + ": " + dataset[0].get("summary", "")
    results = qdrant_client.query_points(collection_name=COLLECTION_NAME, query=Document(text=query_text, model=EMBEDDING_MODEL), using=VECTOR_NAME)
    top = results.points[0]
    print(f"Top score: {top.score:.4f} | Result: {top.payload['document'][:100]}")

    # --- 7. Close Client ---
    qdrant_client.close()
