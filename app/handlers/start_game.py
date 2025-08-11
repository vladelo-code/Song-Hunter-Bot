from aiogram import Dispatcher
from aiogram.types import CallbackQuery
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from app.handlers.game import send_question
from app.dependencies import db_session
from app.db_utils.song import generate_questions
from app.messages.texts import INTRO_GAME
from app.logger import setup_logger

logger = setup_logger(__name__)


async def start_game_handler(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Обрабатывает нажатие на кнопку начала игры.
    - Показывает вводное сообщение с правилами.
    - Генерирует вопросы из базы данных.
    - Инициализирует состояние игры (очки, текущий вопрос, список вопросов, tg_id игрока).
    - Отправляет первый вопрос.
    - Подтверждает callback.

    :param callback: Объект CallbackQuery, инициировавший вызов.
    :param state: FSMContext для работы с состояниями пользователя.
    """
    await callback.message.edit_text(INTRO_GAME, parse_mode='html', reply_markup=None)

    with db_session() as db:
        questions = generate_questions(db)

    # Инициализируем данные игры
    await state.update_data(score=0, current_question=0, questions=questions, tg_id=callback.from_user.id)
    await send_question(callback.message, state)
    await callback.answer()


def register_callback_handler(dp: Dispatcher) -> None:
    """
    Регистрирует обработчики callback-запросов.

    Регистрирует:
    - start_game_handler для callback с data == "start_game", без активного состояния.

    :param dp: Диспетчер aiogram.
    """
    dp.callback_query.register(start_game_handler, lambda c: c.data == "start_game", StateFilter(None))
