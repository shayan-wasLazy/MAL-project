from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base

class User(Base):
    __tablename__ = 'users'
    
    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), index=True, nullable=False)
    email = Column(String(100), unique=True, index=True)
    password = Column(String, nullable=False)
    
class studios(Base):    
    __tablename__ = 'studios'
    
    studio_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    
class Anime(Base):
    __tablename__ = 'anime'
    
    anime_id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    release_year = Column(Integer)
    episodes = Column(Integer)
    studio_id = Column(Integer, ForeignKey('studios.studio_id'))
    
class user_anime(Base):
    __tablename__ = 'user_anime'
    
    user_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True)
    anime_id = Column(Integer, ForeignKey('anime.anime_id'), primary_key=True)
    watch_status = Column(String(20), nullable=False)
    rating = Column(Integer)
    episodes_watched = Column(Integer, default=0)
    
class genres(Base):
    __tablename__ = 'genres'
    
    genre_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    
class anime_genres(Base):
    __tablename__ = 'anime_genres'
    
    anime_id = Column(Integer, ForeignKey('anime.anime_id'), primary_key=True)
    genre_id = Column(Integer, ForeignKey('genres.genre_id'), primary_key=True)