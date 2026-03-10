from fastapi import FastAPI
from sqlalchemy.orm import Session
from fastapi import Depends
from typing import List
from backend.database import engine, SessionLocal
import backend.models as models
import backend.schemas as schemas
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "MAL project is running"}


@app.get("/db-check")
def db_check():
    try:
        conn = engine.connect()
        conn.close()
        return {"status": "Database connected successfully"}
    except Exception as e:
        return {"error": str(e)}

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/anime", response_model=List[schemas.AnimeOut])
def get_anime(db: Session = Depends(get_db)):
    anime_list = db.query(models.Anime).all()
    return anime_list

@app.post("/anime", response_model=schemas.AnimeOut)
def create_anime(
    anime: schemas.AnimeCreate,
    db: Session = Depends(get_db)
):
    new_anime = models.Anime(
        title=anime.title,
        episodes=anime.episodes,
        release_year=anime.release_year,
        studio_id=anime.studio_id
    )

    db.add(new_anime)
    db.commit()
    db.refresh(new_anime)

    return new_anime

