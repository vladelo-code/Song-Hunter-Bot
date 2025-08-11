from sqlalchemy.orm import Session
from typing import Optional, Tuple
from datetime import datetime

from app.models.player import Player


def get_or_create_player(session: Session, tg_id: str, tg_username: str = None) -> Player:
    """
    Получает игрока по Telegram ID или создаёт нового, если не найден.

    :param session: SQLAlchemy сессия для работы с базой данных.
    :param tg_id: Telegram ID пользователя.
    :param tg_username: Никнейм пользователя в Telegram.
    :return: Объект Player из базы данных.
    """
    player = session.query(Player).filter_by(tg_id=tg_id).first()
    if not player:
        player = Player(tg_id=tg_id, tg_username=tg_username, total_games=0, total_score=0)
        session.add(player)
        session.commit()
        session.refresh(player)
    return player


def get_player_stat(session: Session, tg_id: str) -> Optional[Tuple[int, int, datetime, datetime]]:
    """
    Получает статистику игрока из базы данных по Telegram ID.

    :param session: SQLAlchemy сессия для работы с базой данных.
    :param tg_id: Telegram ID игрока.
    :return: Кортеж с общим количеством игр, суммой очков,
             датой первого запуска и датой последней активности,
             либо None, если игрок не найден.
    """
    player_info = session.query(Player).filter_by(tg_id=tg_id).first()
    if player_info:
        return player_info.total_games, player_info.total_score, player_info.first_seen, player_info.last_seen  # type: ignore
    return None


def update_player_stats(session: Session, tg_id: str, score: int):
    """
    Обновляет статистику игрока: увеличивает количество сыгранных игр, сумму очков
    и обновляет время последней активности.

    :param session: SQLAlchemy сессия для работы с базой данных.
    :param tg_id: Telegram ID игрока в базе данных.
    :param score: Очки, набранные в последней игре, которые нужно добавить.
    """
    player = session.query(Player).filter_by(tg_id=tg_id).first()
    if player:
        player.total_games += 1
        player.total_score += score
        player.last_seen = datetime.now()
        session.commit()
