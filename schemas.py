from pydantic import BaseModel
from typing import Optional

class AnimeOut(BaseModel):
    anime_id: int
    title: str
    release_year: Optional[int] = None
    episodes: Optional[int] = None
    studio_id: Optional[int] = None

    class Config:
        orm_mode = True