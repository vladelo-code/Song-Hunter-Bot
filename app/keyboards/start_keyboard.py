from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def start_keyboard() -> InlineKeyboardMarkup:
    """
    Создаёт основную клавиатуру меню стартового экрана бота с кнопками для основных действий:
    - Начать игру
    - Правила игры
    - Мой профиль
    - Рейтинг
    - Статистика треков

    :return: Объект InlineKeyboardMarkup с готовой клавиатурой.
    """
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎮 Начать игру", callback_data="start_game")],
        [InlineKeyboardButton(text="📖 Правила игры", callback_data="rules")],
        [InlineKeyboardButton(text="👤 Мой профиль", callback_data="profile")],
        [InlineKeyboardButton(text="🏆 Рейтинг", callback_data="rating")],
        [InlineKeyboardButton(text="📈 Статистика треков", callback_data="stats_songs")],
    ])
    return keyboard
