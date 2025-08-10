from sqlalchemy import Column, Integer, ForeignKey

from app.models.base import Base


class SongStat(Base):
    __tablename__ = 'song_stats'

    song_id = Column(Integer, ForeignKey('songs.id'), primary_key=True, nullable=False)

    times_played = Column(Integer, default=0, nullable=False)

    correct_count = Column(Integer, default=0, nullable=False)
    wrong_count = Column(Integer, default=0, nullable=False)
