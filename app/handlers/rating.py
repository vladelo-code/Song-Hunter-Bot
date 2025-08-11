from aiogram import Dispatcher
from aiogram.types import CallbackQuery
from aiogram.filters import StateFilter

from app.keyboards.to_home_keyboard import to_home_keyboard
from app.utils.format_rating_stats import format_rating_stats
from app.utils.safe_username import get_safe_username
from app.db_utils.player import get_top_players
from app.dependencies import db_session
from app.messages.texts import STAT_RATING_ERROR
from app.logger import setup_logger

logger = setup_logger(__name__)


async def rating_handler(callback: CallbackQuery) -> None:
    """
    Обработчик нажатия кнопки "🏆 Рейтинг".
    Логирует запрос пользователя и редактирует сообщение,
    показывая рейтинг всех игроков.

    :param callback: Объект CallbackQuery от Telegram.
    """
    username = get_safe_username(callback.from_user.username)
    logger.info(f"🏆 Игрок @{username} запросил рейтинг игроков!")

    with db_session() as db:
        stat = get_top_players(db)

    if not stat:
        stats_message = STAT_RATING_ERROR
    else:
        stats_message = format_rating_stats(stat)

    await callback.message.edit_text(stats_message, parse_mode='html', reply_markup=to_home_keyboard())
    await callback.answer()


def register_callback_handler(dp: Dispatcher) -> None:
    """
    Регистрирует обработчик кнопки "🏆 Рейтинг".

    :param dp: Объект диспетчера aiogram.
    """
    dp.callback_query.register(rating_handler, lambda c: c.data == "rating", StateFilter(None))
