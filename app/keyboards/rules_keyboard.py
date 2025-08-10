from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def rules_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎮 Начать игру", callback_data="start_game")],
        [InlineKeyboardButton(text="🏠 Домой", callback_data="home")],
    ])
    return keyboard
