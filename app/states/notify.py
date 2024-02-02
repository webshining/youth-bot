from aiogram.fsm.state import State, StatesGroup


class Notify(StatesGroup):
    text = State()
