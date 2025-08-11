from aiogram import Dispatcher
from aiogram.types import CallbackQuery
from aiogram.filters import StateFilter

from app.keyboards.start_keyboard import start_keyboard
from app.utils.safe_username import get_safe_username
from app.messages.texts import HOME_MESSAGE
from app.logger import setup_logger

logger = setup_logger(__name__)


async def home_handler(callback: CallbackQuery) -> None:
    """
    Обработчик нажатия кнопки "🏠 Домой".
    Логирует запрос пользователя и возвращает в главное меню.

    :param callback: Объект CallbackQuery от Telegram.
    """
    username = get_safe_username(callback.from_user.username)
    logger.info(f"👋 Игрок @{username} вернулся в главное меню.")
    await callback.message.edit_text(HOME_MESSAGE, parse_mode='html', reply_markup=start_keyboard())
    await callback.answer()


def register_callback_handler(dp: Dispatcher) -> None:
    """
    Регистрирует обработчик кнопки "🏠 Домой".

    :param dp: Объект диспетчера aiogram.
    """
    dp.callback_query.register(home_handler, lambda c: c.data == "home", StateFilter(None))
