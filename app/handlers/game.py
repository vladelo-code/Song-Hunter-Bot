from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.types.input_file import FSInputFile
import time
import os

from app.keyboards.game_keyboard import game_keyboard
from app.keyboards.to_home_keyboard import to_home_from_game_keyboard
from app.states import GameStates
from app.messages.texts import TIME_LIMIT, RIGHT_ANSWER, WRONG_ANSWER, QUESTION, FINISH_GAME

MAX_TIME = 20


async def send_question(message: Message, state: FSMContext) -> None:
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
    data = await state.get_data()
    current = data.get("current_question", 0)
    score = data.get("score", 0)
    questions = data.get("questions")
    start_time = data.get("start_time", time.time())

    elapsed = time.time() - start_time
    if elapsed > MAX_TIME:
        await callback.answer(TIME_LIMIT, show_alert=True)
        await next_question(callback.message, state)
        return

    selected = int(callback.data.split("_")[1])
    correct = questions[current]["correct"]

    if selected == correct:
        points = max(10, int((MAX_TIME - elapsed) * 5))
        score += points
        await callback.answer(RIGHT_ANSWER.format(points))
        await callback.message.edit_reply_markup(reply_markup=game_keyboard(questions[current], selected=selected))
    else:
        await callback.answer(WRONG_ANSWER.format(questions[current]['options'][correct]))
        await callback.message.edit_reply_markup(reply_markup=game_keyboard(questions[current], selected=selected))

    await state.update_data(score=score)
    await next_question(callback.message, state)


async def next_question(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    current = data.get("current_question", 0)
    await state.update_data(current_question=current + 1)
    await send_question(message, state)


async def finish_game(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    score = data.get("score", 0)
    await message.answer(FINISH_GAME.format(score=score), parse_mode="HTML", reply_markup=to_home_from_game_keyboard())
    await state.clear()


def register_callback_handler(dp: Dispatcher) -> None:
    dp.callback_query.register(answer_callback_handler, lambda c: c.data and c.data.startswith("answer_"))
