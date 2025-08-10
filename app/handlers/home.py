from aiogram import Dispatcher
from aiogram.types import CallbackQuery

from app.keyboards.start_keyboard import start_keyboard
from app.messages.texts import NO_USERNAME_USER, HOME_MESSAGE
from app.logger import setup_logger

logger = setup_logger(__name__)


async def show_rules_handler(callback: CallbackQuery) -> None:
    """
    Обработчик нажатия кнопки "🏠 Домой".
    Логирует запрос пользователя и возвращает в главное меню.

    :param callback: Объект CallbackQuery от Telegram.
    """
    username = callback.from_user.username or NO_USERNAME_USER
    logger.info(f"👋 Игрок @{username} вернулся в главное меню.")
    await callback.message.edit_text(HOME_MESSAGE, parse_mode='Markdown', reply_markup=start_keyboard())
    await callback.answer()


def register_callback_handler(dp: Dispatcher) -> None:
    """
    Регистрирует обработчик кнопки "🏠 Домой".

    :param dp: Объект диспетчера aiogram.
    """
    dp.callback_query.register(show_rules_handler, lambda c: c.data == "home")
