from aiogram import Dispatcher

from app.handlers import start


def register_handlers(dp: Dispatcher) -> None:
    """
    Регистрирует все обработчики команд и сообщений для бота.

    :param dp: Экземпляр Dispatcher из aiogram.
    """
    start.register_handler(dp)
