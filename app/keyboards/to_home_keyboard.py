from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def to_home_keyboard() -> InlineKeyboardMarkup:
    """
    Создаёт клавиатуру с кнопками для перехода в главное меню или начала игры.
    Используется для возврата пользователя в домашнее меню из различных разделов.

    :return: Объект InlineKeyboardMarkup с клавиатурой.
    """
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎮 Начать игру", callback_data="start_game")],
        [InlineKeyboardButton(text="🏠 Домой", callback_data="home")],
    ])
    return keyboard


def to_home_from_game_keyboard() -> InlineKeyboardMarkup:
    """
    Создаёт клавиатуру с кнопками для начала новой игры или возврата в главное меню.
    Используется после завершения игровой сессии.

    :return: Объект InlineKeyboardMarkup с клавиатурой.
    """
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎮 Сыграть ещё", callback_data="start_game")],
        [InlineKeyboardButton(text="🏠 Домой", callback_data="home")],
    ])
    return keyboard
