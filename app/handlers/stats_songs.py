from aiogram import Dispatcher
from aiogram.types import CallbackQuery
from aiogram.filters import StateFilter

from app.keyboards.to_home_keyboard import to_home_keyboard
from app.utils.format_song_stats import format_song_stats
from app.utils.safe_username import get_safe_username
from app.db_utils.stats_songs import get_most_guessed_songs
from app.dependencies import db_session
from app.messages.texts import STAT_MUSIC_ERROR
from app.logger import setup_logger

logger = setup_logger(__name__)


async def stats_songs_handler(callback: CallbackQuery) -> None:
    """
    Обработчик нажатия кнопки "📈 Статистика треков".
    Логирует запрос пользователя и редактирует сообщение,
    показывая статистику игрока.

    :param callback: Объект CallbackQuery от Telegram.
    """
    username = get_safe_username(callback.from_user.username)
    logger.info(f"📈 Игрок @{username} запросил статистику треков!")

    with db_session() as db:
        stat = get_most_guessed_songs(db)

    if not stat:
        stats_message = STAT_MUSIC_ERROR
    else:
        stats_message = format_song_stats(stat)

    await callback.message.edit_text(stats_message, parse_mode='html', reply_markup=to_home_keyboard())
    await callback.answer()


def register_callback_handler(dp: Dispatcher) -> None:
    """
    Регистрирует обработчик кнопки "📈 Статистика треков".

    :param dp: Объект диспетчера aiogram.
    """
    dp.callback_query.register(stats_songs_handler, lambda c: c.data == "stats_songs", StateFilter(None))
