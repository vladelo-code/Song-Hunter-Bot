from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.filters import Command

from app.logger import setup_logger

logger = setup_logger(__name__)


async def start_command(message: Message) -> None:
    """
    Обрабатывает команду /start
    - Регистрирует или обновляет информацию об игроке.
    - Отправляет приветственное сообщение.

    :param message: Объект входящего сообщения от пользователя.
    """
    logger.info(f"👋 Игрок @{message.from_user.username} запустил бота!")

    # with db_session() as db:
    #     register_or_update_player(db, telegram_id=str(message.from_user.id), username=message.from_user.username)

    await message.answer("Привет!")


def register_handler(dp: Dispatcher) -> None:
    """
    Регистрирует обработчики команд и кнопок:
    - /start — запуск бота
    - '🏠 Главное меню' — возврат в главное меню
    - '🚓 Правила игры' — показ правил игры

    :param dp: Объект диспетчера aiogram.
    """
    dp.message.register(start_command, Command("start"))
