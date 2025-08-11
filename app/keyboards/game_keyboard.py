from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def game_keyboard(question: dict, selected: int = None) -> InlineKeyboardMarkup:
    """
    Формирует клавиатуру с вариантами ответа для текущего вопроса.

    Если выбран ответ (selected не None), то:
        - Помечает правильный ответ галочкой ✅
        - Помечает выбранный неправильный ответ крестиком ❌
        - Все кнопки становятся неактивными (callback_data = "ignored")

    Если ответ не выбран, то:
        - Кнопки активны с callback_data "answer_i", где i — индекс варианта.

    Кнопки группируются по 2 в ряд.

    :param question: Словарь с данными вопроса, включая варианты ответов и индекс правильного.
    :param selected: Индекс выбранного варианта ответа или None, если ответ ещё не выбран.
    :return: Объект InlineKeyboardMarkup для отправки в Telegram.
    """
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
