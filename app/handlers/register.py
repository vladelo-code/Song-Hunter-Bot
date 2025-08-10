from aiogram import Dispatcher

from app.handlers import start, start_game, rules


def register_handlers(dp: Dispatcher) -> None:
    """
    Регистрирует все обработчики команд и сообщений для бота.

    :param dp: Экземпляр Dispatcher из aiogram.
    """
    start.register_handler(dp)
    start_game.register_callback_handler(dp)
    rules.register_callback_handler(dp)
