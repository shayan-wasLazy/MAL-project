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

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

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

# @app.post("/anime", response_model=schemas.AnimeOut)
# def create_anime(
#     anime: schemas.AnimeCreate,
#     db: Session = Depends(get_db)
# ):
#     new_anime = models.Anime(
#         title=anime.title,
#         episodes=anime.episodes,
#         release_year=anime.release_year,
#         studio_id=anime.studio_id
#     )

#     db.add(new_anime)
#     db.commit()
#     db.refresh(new_anime)

#     return new_anime

