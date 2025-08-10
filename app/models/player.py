from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from app.models.base import Base


class Player(Base):
    __tablename__ = 'players'

    id = Column(Integer, primary_key=True, autoincrement=True)

    tg_id = Column(String, unique=True, nullable=False)
    tg_username = Column(String, nullable=True)

    total_games = Column(Integer, default=0, nullable=False)
    total_score = Column(Integer, default=0, nullable=False)

    first_seen = Column(DateTime, default=datetime.now, nullable=False)
    last_seen = Column(DateTime, default=datetime.now, nullable=False)
