from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.filters import Command

from app.keyboards.start_keyboard import start_keyboard
from app.utils.safe_username import get_safe_username
from app.dependencies import db_session
from app.db_utils.player import get_or_create_player
from app.messages.texts import WELCOME_MESSAGE
from app.logger import setup_logger

logger = setup_logger(__name__)


async def start_command(message: Message) -> None:
    """
    Обрабатывает команду /start
    - Регистрирует или обновляет информацию об игроке.
    - Отправляет приветственное сообщение с inline-кнопка для дальнейшей навигации.

    :param message: Объект входящего сообщения от пользователя.
    """
    username = get_safe_username(message.from_user.username)
    logger.info(f"👋 Игрок @{username} запустил бота!")

    with db_session() as db:
        get_or_create_player(db, tg_id=str(message.from_user.id), tg_username=username)

    await message.answer(WELCOME_MESSAGE, parse_mode='html', reply_markup=start_keyboard())


def register_handler(dp: Dispatcher) -> None:
    """
    Регистрирует обработчики команд и кнопок:
    - /start — запуск бота

    :param dp: Объект диспетчера aiogram.
    """
    dp.message.register(start_command, Command("start"))
