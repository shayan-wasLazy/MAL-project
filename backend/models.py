from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Date
from backend.database import Base

class User(Base):
    __tablename__ = 'users'
    
    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), index=True, nullable=False)
    email = Column(String(100), unique=True, index=True)
    password = Column(String, nullable=False)
    
# class studios(Base):    
#     __tablename__ = 'studios'
    
#     studio_id = Column(Integer, primary_key=True, index=True)
#     name = Column(String(100), nullable=False)
    
class Anime(Base):
    __tablename__ = 'animes'
    
    anime_id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    score = Column(Integer)
    rank = Column(Integer)
    popularity = Column(Integer)
    members = Column(Integer)
    synopsis = Column(String)
    start_date = Column(Date)
    end_date = Column(Date)
    type = Column(String(20))
    episodes = Column(Integer)
    image_url = Column(String)
    
class user_anime(Base):
    __tablename__ = 'user_anime'
    
    user_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True)
    anime_id = Column(Integer, ForeignKey('anime.anime_id'), primary_key=True)
    watch_status = Column(String(20), nullable=False)
    rating = Column(Integer)
    episodes_watched = Column(Integer, default=0)
    
# class genres(Base):
#     __tablename__ = 'genres'
    
#     genre_id = Column(Integer, primary_key=True, index=True)
#     name = Column(String(50), nullable=False)
    
# class anime_genres(Base):
#     __tablename__ = 'anime_genres'
    
#     anime_id = Column(Integer, ForeignKey('anime.anime_id'), primary_key=True)
#     genre_id = Column(Integer, ForeignKey('genres.genre_id'), primary_key=True)