# qdrant_utils.py
"""
Utilities to interact with Qdrant Cloud.
Handles:
- Connecting to Qdrant
- Creating collections
- Inserting embeddings
- Searching by similarity
"""

from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct, VectorParams, Filter, FieldCondition, MatchValue
import os

# ---------------------------
# 1. Load Qdrant credentials from environment
# ---------------------------
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
COLLECTION_NAME = "document_chatbot"

# ---------------------------
# 2. Connect to Qdrant
# ---------------------------
client = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY
)

# ---------------------------
# 3. Create collection if it doesn't exist
# ---------------------------
if COLLECTION_NAME not in [c.name for c in client.get_collections().collections]:
    client.recreate_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=384, distance="Cosine"),  # 384 = all-MiniLM-L6-v2 embedding size
        optimizers_config=None
    )

# ---------------------------
# 4. Insert embeddings
# ---------------------------
def insert_embeddings(vectors: list[dict], source: str = "unknown"):
    """
    Insert a list of embeddings into Qdrant.
    Each dict in vectors must have: id, embedding, text, source
    """
    points = [
        PointStruct(
            id=v["id"],
            vector=v["embedding"],
            payload={"text": v["text"], "source": v["source"]}
        )
        for v in vectors
    ]
    client.upsert(collection_name=COLLECTION_NAME, points=points)

# ---------------------------
# 5. Search embeddings
# ---------------------------
def search_embeddings(query: str, top_k: int = 3) -> list[dict]:
    """
    Convert query to embedding (use embeddings.py)
    Search Qdrant for top_k similar vectors
    Returns list of dicts with 'text' and 'source'
    """
    from embeddings import get_embeddings

    query_vec = get_embeddings(query)[0]["embedding"]  # single vector for query

    results = client.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_vec,
        limit=top_k
    )

    # Return only the text and source for simplicity
    return [{"text": r.payload["text"], "source": r.payload["source"]} for r in results]
