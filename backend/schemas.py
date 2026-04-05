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
        
# class AnimeCreate(BaseModel):
#     title: str
#     episodes: int | None = None
#     release_year: int | None = None
#     studio_id: int | None = None
    
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