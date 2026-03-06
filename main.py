from fastapi import FastAPI
from database import engine
from sqlalchemy.orm import Session
from fastapi import Depends
from database import SessionLocal
from typing import List
import schemas
import models

app = FastAPI()

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

