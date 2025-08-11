from aiogram import Dispatcher, types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types.input_file import FSInputFile
import time
import os

from app.db_utils.song import generate_questions
from app.dependencies import db_session
from app.keyboards.game_keyboard import game_keyboard


class GameStates(StatesGroup):
    WAIT_ANSWER = State()


MAX_TIME = 20  # секунд на ответ


async def start_game_handler(callback: types.CallbackQuery, state: FSMContext) -> None:
    with db_session() as db:
        questions = generate_questions(db)

    # Инициализируем данные игры
    await state.update_data(score=0, current_question=0, questions=questions)
    await send_question(callback.message, state)
    await callback.answer()


async def send_question(message: types.Message, state: FSMContext) -> None:
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

    # Отправляем вопрос с кнопками
    await message.answer(
        f"Вопрос {current + 1} из {len(questions)}.\n"
        f"У тебя есть {MAX_TIME} секунд, чтобы ответить.",
        reply_markup=game_keyboard(question),
    )
    await state.set_state(GameStates.WAIT_ANSWER)
    await state.update_data(start_time=time.time())


async def answer_callback_handler(callback: types.CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    current = data.get("current_question", 0)
    score = data.get("score", 0)
    questions = data.get("questions")
    start_time = data.get("start_time", time.time())

    elapsed = time.time() - start_time
    if elapsed > MAX_TIME:
        await callback.answer("Время вышло! Ответ не засчитан.", show_alert=True)
        await next_question(callback.message, state)
        return

    selected = int(callback.data.split("_")[1])
    correct = questions[current]["correct"]

    if selected == correct:
        points = max(1, int((MAX_TIME - elapsed) * 10))  # пример: максимум 200 очков
        score += points
        await callback.answer(f"Верно! Ты заработал {points} очков.")
        await callback.message.edit_reply_markup(reply_markup=game_keyboard(questions[current], selected=selected))
    else:
        await callback.answer(f"Неверно! Правильный ответ: {questions[current]['options'][correct]}")
        await callback.message.edit_reply_markup(reply_markup=game_keyboard(questions[current], selected=selected))

    await state.update_data(score=score)
    await next_question(callback.message, state)


async def next_question(message: types.Message, state: FSMContext) -> None:
    data = await state.get_data()
    current = data.get("current_question", 0)
    await state.update_data(current_question=current + 1)
    await send_question(message, state)


async def finish_game(message: types.Message, state: FSMContext) -> None:
    data = await state.get_data()
    score = data.get("score", 0)
    await message.answer(f"Игра окончена! Твой итоговый счет: <b>{score}</b>.", parse_mode="HTML")
    await state.clear()


def register_callback_handler(dp: Dispatcher) -> None:
    dp.callback_query.register(start_game_handler, lambda c: c.data == "start_game", StateFilter(None))
    dp.callback_query.register(answer_callback_handler, lambda c: c.data and c.data.startswith("answer_"))
