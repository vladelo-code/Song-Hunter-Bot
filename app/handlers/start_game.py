from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from app.handlers.game import send_question
from app.dependencies import db_session
from app.logger import setup_logger

logger = setup_logger(__name__)

from app.db_utils.song import generate_questions


async def start_game_handler(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.message.edit_text(
        "Игра запускается!",
        reply_markup=None
    )

    with db_session() as db:
        questions = generate_questions(db)

    # Инициализируем данные игры
    await state.update_data(score=0, current_question=0, questions=questions)
    await send_question(callback.message, state)
    await callback.answer()


def register_callback_handler(dp: Dispatcher) -> None:
    """
    Регистрирует обработчики команд и кнопок:
    - /start — запуск бота

    :param dp: Объект диспетчера aiogram.
    """
    dp.callback_query.register(start_game_handler, lambda c: c.data == "start_game", StateFilter(None))
