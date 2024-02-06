from aiogram.fsm.state import State, StatesGroup


class NeedState(StatesGroup):
    name = State()
    text = State()
