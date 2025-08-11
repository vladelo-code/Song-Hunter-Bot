from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def to_home_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎮 Начать игру", callback_data="start_game")],
        [InlineKeyboardButton(text="🏠 Домой", callback_data="home")],
    ])
    return keyboard


def to_home_from_game_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎮 Сыграть ещё", callback_data="start_game")],
        [InlineKeyboardButton(text="🏠 Домой", callback_data="home")],
    ])
    return keyboard
