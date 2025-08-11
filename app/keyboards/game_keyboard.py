from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def game_keyboard(question: dict, selected: int = None) -> InlineKeyboardMarkup:
    buttons = []
    if selected is not None:
        for i, option in enumerate(question["options"]):
            text = option
            if i == question["correct"]:
                text = "✅ " + text
            elif i == selected:
                text = "❌ " + text
            buttons.append(InlineKeyboardButton(text=text, callback_data="ignored"))
    else:
        for i, option in enumerate(question["options"]):
            buttons.append(InlineKeyboardButton(text=option, callback_data=f"answer_{i}"))

    inline_keyboard = [buttons[i:i + 2] for i in range(0, len(buttons), 2)]

    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
