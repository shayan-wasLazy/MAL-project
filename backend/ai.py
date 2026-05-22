from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient

qdrant = QdrantClient(
    host="localhost",
    port=6333
)

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)