from sqlalchemy import Column, Integer, ForeignKey, DateTime
from datetime import datetime

from app.models.base import Base


class GameSession(Base):
    __tablename__ = 'game_sessions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    player_id = Column(Integer, ForeignKey('players.id'), nullable=False)

    score = Column(Integer, default=0, nullable=False)
    questions_count = Column(Integer, default=0, nullable=False)

    played_at = Column(DateTime, default=datetime.now, nullable=False)
