from aiogram.fsm.state import State, StatesGroup


class GameStates(StatesGroup):
    WAIT_ANSWER = State()
