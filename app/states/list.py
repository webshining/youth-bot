from aiogram.fsm.state import State, StatesGroup


class ListState(StatesGroup):
    create_name = State()
    edit_name = State()
    send_message = State()
