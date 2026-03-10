from pydantic import BaseModel
from typing import Optional

class AnimeOut(BaseModel):
    anime_id: int
    title: str
    release_year: Optional[int] = None
    episodes: Optional[int] = None
    studio_id: Optional[int] = None

    class Config:
        from_attributes = True
        
class AnimeCreate(BaseModel):
    title: str
    episodes: int | None = None
    release_year: int | None = None
    studio_id: int | None = None