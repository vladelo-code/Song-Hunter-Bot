from aiogram import Dispatcher
from aiogram.types import CallbackQuery

from app.keyboards.rules_keyboard import rules_keyboard
from app.messages.texts import RULES, NO_USERNAME_USER
from app.logger import setup_logger

logger = setup_logger(__name__)


async def show_rules_handler(callback: CallbackQuery) -> None:
    """
    Обработчик нажатия кнопки "📖 Правила игры".
    Логирует запрос пользователя и редактирует сообщение,
    показывая текст правил с клавиатурой.

    :param callback: Объект CallbackQuery от Telegram.
    """
    username = callback.from_user.username or NO_USERNAME_USER
    logger.info(f"👋 Игрок @{username} запросил правила игры!")
    await callback.message.edit_text(RULES, parse_mode='Markdown', reply_markup=rules_keyboard())
    await callback.answer()


def register_callback_handler(dp: Dispatcher) -> None:
    """
    Регистрирует обработчик кнопки "📖 Правила игры".

    :param dp: Объект диспетчера aiogram.
    """
    dp.callback_query.register(show_rules_handler, lambda c: c.data == "rules")
