from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.models import Distance, PointStruct, VectorParams
from backend.database import SessionLocal
import backend.models as models
from tqdm import tqdm

db = SessionLocal()


model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

print("Model loaded successfully.")

qdrant = QdrantClient(
    host="localhost",
    port=6333
)

print("Qdrant client initialized successfully.")


collections = qdrant.get_collections().collections

existing_collections = [
    collection.name
    for collection in collections
]

if "anime_embeddings" not in existing_collections:

    qdrant.create_collection(
        collection_name="anime_embeddings",
        vectors_config=VectorParams(
            size=384,
            distance=Distance.COSINE
        )
    )

    print("Collection created.")

else:
    print("Collection already exists.")

print("Qdrant collection created successfully.")


anime = models.Anime
anime_rows = db.query(anime).all()

points = []

for anime in tqdm(anime_rows, desc="Processing anime embeddings"):

    # print(anime.title)
    
    combined_text = f"""
    Title: {anime.title or ""}

    Genres: {anime.genres or ""}

    Tags: {anime.tags or ""}

    Studios: {anime.studios or ""}

    Synopsis:
    {anime.sysnopsis or ""}
    """
    
    
    # print(f"Successfully combined text for anime ID: {anime.anime_id} || Title: {anime.title}")
    embedding = model.encode(combined_text)
    
    point = PointStruct(
    id=anime.anime_id,
    vector=embedding.tolist(),
    payload={
        "anime_id": anime.anime_id,
        "title": anime.title,
        "genres": anime.genres
    }
    )

    points.append(point)
    
from tqdm import tqdm

BATCH_SIZE = 100

for i in tqdm(
    range(0, len(points), BATCH_SIZE),
    desc="Uploading to Qdrant"
):

    batch = points[i:i + BATCH_SIZE]

    qdrant.upsert(
        collection_name="anime_embeddings",
        points=batch
    )

print("Embeddings uploaded successfully.")