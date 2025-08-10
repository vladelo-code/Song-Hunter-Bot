from sqlalchemy.orm import Session
from datetime import datetime

from app.models.player import Player


def get_or_create_player(session: Session, tg_id: int, tg_username: str) -> Player:
    player = session.query(Player).filter_by(tg_id=tg_id).first()
    if not player:
        player = Player(tg_id=str(tg_id), tg_username=tg_username, total_games=0, total_score=0)
        session.add(player)
        session.commit()
        session.refresh(player)
    return player


def update_player_stats(session: Session, player_id: int, score: int):
    player = session.query(Player).get(player_id)
    if player:
        player.total_games += 1
        player.total_score += score
        player.last_seen = datetime.now()
        session.commit()
