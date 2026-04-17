from fastapi import FastAPI, HTTPException
from sqlalchemy.orm import Session
from fastapi import Depends
from typing import List
from backend.database import engine, SessionLocal
import backend.models as models
import backend.schemas as schemas
from fastapi.middleware.cors import CORSMiddleware
import hashlib

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


@app.post("/register", response_model=schemas.UserOut)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(models.User.username == user.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already taken")
    new_user = models.User(
        username=user.username,
        email=user.email,
        password=hash_password(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/login", response_model=schemas.UserOut)
def login(credentials: schemas.LoginRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == credentials.username).first()
    if not user or user.password != hash_password(credentials.password):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return user

@app.get("/user/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.user_id == user_id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user

@app.get("/user/{user_id}/anime")
def get_user_anime(user_id: int, db: Session = Depends(get_db)):

    results = db.query(
        models.UserAnime,
        models.Anime.title,
        models.Anime.image_url
    ).join(
        models.Anime,
        models.UserAnime.anime_id == models.Anime.anime_id
    ).filter(
        models.UserAnime.user_id == user_id
    ).all()

    return [
        {
            "anime_id": ua.anime_id,
            "title": title,
            "image_url": image_url,
            "watch_status": ua.watch_status,
            "rating": ua.rating,
            "episodes_watched": ua.episodes_watched
        }
        for ua, title, image_url in results
    ]

@app.get("/anime/{id}")
def get_anime(id: int, db: Session = Depends(get_db)):
    return db.query(models.Anime).filter(models.Anime.anime_id == id).first()

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

@app.post("/user_anime")
def add_user_anime(entry: schemas.UserAnimeCreate, db: Session = Depends(get_db)):

    existing = db.query(models.UserAnime).filter(
        models.UserAnime.user_id == entry.user_id,
        models.UserAnime.anime_id == entry.anime_id
    ).first()

    if existing:
        # UPDATE instead of error
        existing.watch_status = entry.watch_status
        existing.rating = entry.rating
        existing.episodes_watched = entry.episodes_watched
    else:
        new_entry = models.UserAnime(
            user_id=entry.user_id,
            anime_id=entry.anime_id,
            watch_status=entry.watch_status,
            rating=entry.rating,
            episodes_watched=entry.episodes_watched
        )
        db.add(new_entry)

    db.commit()

    return {"message": "Saved successfully"}
