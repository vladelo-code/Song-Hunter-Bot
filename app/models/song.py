from sqlalchemy import Column, Integer, String
from app.models.base import Base


class Song(Base):
    __tablename__ = 'songs'

    id = Column(Integer, primary_key=True, autoincrement=True)

    title = Column(String, nullable=False)
    artist = Column(String, nullable=False)
    category = Column(String, nullable=True)
    year = Column(Integer, nullable=True)

    clip_path = Column(String, nullable=False)
    full_path = Column(String, nullable=True)
