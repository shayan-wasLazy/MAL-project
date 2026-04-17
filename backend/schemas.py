from pydantic import BaseModel
from datetime import date
from typing import Optional


class AnimeOut(BaseModel):
    anime_id: int
    title: str
    start_date: Optional[date] = None
    score : Optional[int] = None
    rank : Optional[int] = None
    popularity : Optional[int] = None
    synopsis : str
    type : str
    episodes : Optional[int] = None
    image_url : str

    class Config:
        from_attributes = True
        
class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class LoginRequest(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    user_id: int
    username: str

    class Config:
        from_attributes = True
        
class UserAnimeCreate(BaseModel):
    user_id: int
    anime_id: int
    watch_status: str
    rating: int | None = None
    episodes_watched: int = 0