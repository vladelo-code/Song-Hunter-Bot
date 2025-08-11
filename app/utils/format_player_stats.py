def format_player_stats(total_games: int, total_score: int, first_seen, last_seen) -> str:
    """
    Форматирует статистику игрока в удобочитаемый HTML-текст.

    :param total_games: Общее количество сыгранных игр.
    :param total_score: Общий накопленный счёт игрока.
    :param first_seen: Дата и время первого запуска (datetime).
    :param last_seen: Дата и время последней активности (datetime).
    :return: Отформатированная строка с HTML-разметкой.
    """
    return (
        f"<b>📊 Ваша статистика:</b>\n\n"
        f"• Всего игр: <b>{total_games}</b>\n"
        f"• Общий счёт: <b>{total_score}</b>\n"
        f"• Первый запуск: <b>{first_seen.strftime('%d.%m.%Y')}</b>\n"
        f"• Последняя активность: <b>{last_seen.strftime('%d.%m.%Y')}</b>"
    )
