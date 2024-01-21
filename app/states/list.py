from aiogram.fsm.state import State, StatesGroup


class ListStates(StatesGroup):
    create_name = State()
