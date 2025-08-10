from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from app.keyboards.start_keyboard import start_keyboard
from app.dependencies import db_session
from app.logger import setup_logger

logger = setup_logger(__name__)


async def start_game_handler(callback: CallbackQuery) -> None:
    await callback.message.edit_text(
        "Игра запускается!",
        reply_markup=None
    )

    await callback.answer()


def register_callback_handler(dp: Dispatcher) -> None:
    """
    Регистрирует обработчики команд и кнопок:
    - /start — запуск бота

    :param dp: Объект диспетчера aiogram.
    """

    dp.callback_query.register(start_game_handler, lambda c: c.data == "start_game")
