from aiogram.fsm.state import State, StatesGroup


class GameStates(StatesGroup):
    """
    Класс состояний для игры.
    Используется для управления состояниями FSM в процессе игры.
    """
    WAIT_ANSWER = State()
