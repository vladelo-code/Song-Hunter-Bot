def format_player_stats(total_games: int, total_score: int, first_seen, last_seen) -> str:
    return (
        f"<b>📊 Ваша статистика:</b>\n\n"
        f"• Всего игр: <b>{total_games}</b>\n"
        f"• Общий счёт: <b>{total_score}</b>\n"
        f"• Первый запуск: <b>{first_seen.strftime('%d.%m.%Y %H:%M')}</b>\n"
        f"• Последняя активность: <b>{last_seen.strftime('%d.%m.%Y %H:%M')}</b>"
    )
