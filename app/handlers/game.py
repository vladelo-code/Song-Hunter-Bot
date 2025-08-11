from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.types.input_file import FSInputFile
import time
import os

from app.db_utils.game import add_game
from app.utils.safe_username import get_safe_username
from app.db_utils.player import update_player_stats
from app.db_utils.stats_songs import update_song_stats
from app.dependencies import db_session
from app.keyboards.game_keyboard import game_keyboard
from app.keyboards.to_home_keyboard import to_home_from_game_keyboard
from app.states import GameStates
from app.messages.texts import TIME_LIMIT, RIGHT_ANSWER, WRONG_ANSWER, QUESTION, FINISH_GAME
from app.logger import setup_logger

logger = setup_logger(__name__)

MAX_TIME = 20


async def send_question(message: Message, state: FSMContext) -> None:
    """
    Отправляет текущий вопрос игроку.
    - Проверяет текущий индекс вопроса.
    - Если вопросы закончились, завершает игру.
    - Отправляет аудио (голосовое сообщение) с отрывком трека.
    - Отправляет текст с номером вопроса и временем на ответ.
    - Устанавливает состояние ожидания ответа.
    - Записывает время начала вопроса в состояние.

    :param message: Объект Message для отправки сообщений.
    :param state: FSMContext для доступа и обновления состояния игры.
    """
    data = await state.get_data()
    current = data.get("current_question", 0)
    questions = data.get("questions")

    if current >= len(questions):
        await finish_game(message, state)
        return

    question = questions[current]

    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    clip_abs_path = os.path.join(base_dir, question["clip_path"])

    if os.path.exists(clip_abs_path):
        await message.answer_voice(FSInputFile(str(clip_abs_path)))
    else:
        await message.answer(f"Ошибка: файл {question['clip_path']} не найден.")

    await message.answer(QUESTION.format(question=current + 1, lenght=len(questions), time=MAX_TIME),
                         parse_mode="HTML",
                         reply_markup=game_keyboard(question))
    await state.set_state(GameStates.WAIT_ANSWER)
    await state.update_data(start_time=time.time())


async def answer_callback_handler(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Обрабатывает ответ пользователя на вопрос.
    - Проверяет время ответа, при превышении времени сообщает и переходит к следующему вопросу.
    - Определяет выбранный вариант и правильный ответ.
    - Начисляет или списывает очки в зависимости от правильности.
    - Обновляет статистику по треку в базе данных.
    - Обновляет отображение кнопок с отмеченным ответом.
    - Обновляет текущий счет в состоянии.
    - Переходит к следующему вопросу.

    :param callback: CallbackQuery с ответом пользователя.
    :param state: FSMContext для доступа к состоянию игры.
    """
    data = await state.get_data()
    current = data.get("current_question", 0)
    score = data.get("score", 0)
    questions = data.get("questions")
    song_id = questions[current]["song_id"]
    start_time = data.get("start_time", time.time())

    elapsed = time.time() - start_time
    if elapsed > MAX_TIME:
        await callback.answer(TIME_LIMIT, show_alert=True)
        await next_question(callback.message, state)
        return

    selected = int(callback.data.split("_")[1])
    correct = questions[current]["correct"]

    if selected == correct:
        points = max(1, int(MAX_TIME - elapsed))
        score += points
        correct_answered = True
        await callback.answer(RIGHT_ANSWER.format(points=points))
        await callback.message.edit_reply_markup(reply_markup=game_keyboard(questions[current], selected=selected))
    else:
        score -= 10
        correct_answered = False
        await callback.answer(WRONG_ANSWER.format(answer=questions[current]['options'][correct]))
        await callback.message.edit_reply_markup(reply_markup=game_keyboard(questions[current], selected=selected))

    with db_session() as db:
        update_song_stats(db, song_id, correct_answered)

    await state.update_data(score=score)
    await next_question(callback.message, state)


async def next_question(message: Message, state: FSMContext) -> None:
    """
    Переходит к следующему вопросу.
    - Увеличивает счетчик текущего вопроса.
    - Отправляет следующий вопрос игроку.

    :param message: Объект Message для отправки сообщений.
    :param state: FSMContext для доступа к состоянию игры.
    """
    data = await state.get_data()
    current = data.get("current_question", 0)
    await state.update_data(current_question=current + 1)
    await send_question(message, state)


async def finish_game(message: Message, state: FSMContext) -> None:
    """
    Завершает игру.
    - Считывает итоговый счет из состояния.
    - Сохраняет игру и обновляет статистику игрока в базе данных.
    - Отправляет сообщение с итогами игроку.
    - Очищает состояние FSM.

    :param message: Объект Message для отправки сообщений.
    :param state: FSMContext для очистки состояния.
    """
    data = await state.get_data()
    score = data.get("score", 0)
    tg_id = data.get("tg_id")

    with db_session() as db:
        add_game(db, str(tg_id), score)
        update_player_stats(db, str(tg_id), score)
    logger.info(f"🎯 Игрок с id:{tg_id} закончил игру с результатом: {score}")
    await message.answer(FINISH_GAME.format(score=score), parse_mode="HTML", reply_markup=to_home_from_game_keyboard())
    await state.clear()


def register_callback_handler(dp: Dispatcher) -> None:
    """
    Регистрирует обработчик callback-запросов для ответов на вопросы игры.

    :param dp: Объект Dispatcher для регистрации обработчиков.
    """
    dp.callback_query.register(answer_callback_handler, lambda c: c.data and c.data.startswith("answer_"))
