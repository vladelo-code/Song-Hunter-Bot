from aiogram import Dispatcher
from aiogram.types import CallbackQuery
from aiogram.filters import StateFilter

from app.keyboards.to_home_keyboard import to_home_keyboard
from app.utils.safe_username import get_safe_username
from app.utils.format_player_stats import format_player_stats
from app.db_utils.player import get_player_stat
from app.dependencies import db_session
from app.messages.texts import STAT_ERROR
from app.logger import setup_logger

logger = setup_logger(__name__)


async def profile_handler(callback: CallbackQuery) -> None:
    """
    Обработчик нажатия кнопки "👤 Мой профиль".
    Логирует запрос пользователя и редактирует сообщение,
    показывая статистику игрока.

    :param callback: Объект CallbackQuery от Telegram.
    """
    username = get_safe_username(callback.from_user.username)
    logger.info(f"👋 Игрок @{username} запросил свою статистику!")

    with db_session() as db:
        stat = get_player_stat(db, tg_id=str(callback.from_user.id))

    if not stat:
        stats_message = STAT_ERROR
    else:
        stats_message = format_player_stats(*stat)

    await callback.message.edit_text(stats_message, parse_mode='html', reply_markup=to_home_keyboard())
    await callback.answer()


def register_callback_handler(dp: Dispatcher) -> None:
    """
    Регистрирует обработчик кнопки "👤 Мой профиль".

    :param dp: Объект диспетчера aiogram.
    """
    dp.callback_query.register(profile_handler, lambda c: c.data == "profile", StateFilter(None))
