from sqlalchemy.orm import Session

from app.db_utils.player import get_or_create_player
from app.models.game_session import GameSession


def add_game(session: Session, tg_id: str, score: int, questions_count: int = 5) -> None:
    player = get_or_create_player(session, tg_id)
    game = GameSession(player_id=player.id, score=score, questions_count=questions_count)
    session.add(game)
    session.commit()
    session.refresh(game)
