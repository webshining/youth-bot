from aiogram.fsm.state import State, StatesGroup


class GroupState(StatesGroup):
    create_name = State()
    edit_name = State()

    send_message = State()
