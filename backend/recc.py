from backend.database import SessionLocal
import backend.models as models
from backend.ai import model, qdrant

# from backend.embeddings import qdrant



def anime_reccomend(name: str):
    anime = models.Anime
    db = SessionLocal()
    anime_name = db.query(anime).filter(anime.title == name).first()
    if not anime_name:
        print("Anime not found")
        return

    combined_text = f"""
    Title: {anime_name.title or ""}

    Genres: {anime_name.genres or ""}

    Tags: {anime_name.tags or ""}

    Studios: {anime_name.studios or ""}

    Synopsis:
    {anime_name.sysnopsis or ""}
    """
    query_embedding = model.encode(
    combined_text
    )
    results = qdrant.query_points(
    collection_name="anime_embeddings",
    query=query_embedding,
    limit=6
    ).points
    
    
    reccomendations = []
    
    for result in results:
        if result.payload["anime_id"] != anime_name.anime_id:
            reccomendations.append(
                {
                    "anime_id": result.payload["anime_id"]
                }
            )
            
    return reccomendations


# name = "One Punch Man"            
# anime_reccomend(name)