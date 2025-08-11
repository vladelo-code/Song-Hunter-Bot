from app.models import Player


def format_song_stats(stats_with_songs: list[Player]) -> str:
    """
    Форматирует список статистики по песням в читаемый текст для вывода в Telegram.

    :param stats_with_songs: Список кортежей (статистика, песня), где
                             статистика содержит поля correct_count и times_played,
                             песня содержит title и artist.
    :return: Строка с форматированной статистикой топ 10 песен.
    """
    lines = ["📊 <b>Топ 10 самых угадываемых треков:</b>\n"]
    for i, (stat, song) in enumerate(stats_with_songs, 1):
        accuracy = int((stat.correct_count / stat.times_played) * 100) if stat.times_played > 0 else 0
        trophy = " 🏆" if i == 1 else ""

        line = (
            f"{i:2d}. {trophy} <b>{song.title}</b> — <b>{song.artist}</b>\n"
            f"     👀Точность угадывания: <tg-spoiler>{accuracy}%</tg-spoiler>"
        )
        lines.append(line)
        lines.append("")

    return "\n".join(lines)
