from app.utils.safe_username import get_safe_username


def format_game_stats(games: list[tuple]) -> str:
    """
    Форматирует список лучших игровых сессий в красивый текстовый топ.

    :param games: Список кортежей вида (tg_username: str, score: int, played_at: datetime),
                  например, результат функции get_top_5_best_games().
    :return: Отформатированная строка с топом игровых сессий.
    """
    lines = ["⚡ <b>Топ игр по результату за одну игру:</b>\n"]
    for i, (username_raw, score) in enumerate(games, 1):
        username = get_safe_username(username_raw)
        lines.append(f"{i}. <b>@{username}</b> — <tg-spoiler>{score}</tg-spoiler> очков")
    return "\n".join(lines)
