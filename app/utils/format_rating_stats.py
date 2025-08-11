from app.models import Player
from app.utils.safe_username import get_safe_username


def format_rating_stats(players: list[Player]) -> str:
    """
    Форматирует список игроков в красивый текстовый рейтинг.

    :param players: Список объектов Player.
    :return: Отформатированная строка с рейтингом игроков.
    """
    lines = ["🏆 <b>Топ игроков по сумме очков:</b>\n"]
    for i, player in enumerate(players, 1):
        username = get_safe_username(player.tg_username)
        score = player.total_score
        lines.append(f"{i}. <b>@{username}</b> — <tg-spoiler>{score}</tg-spoiler> очков")
    return "\n".join(lines)
