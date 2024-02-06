from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from loader import dp


@dp.message(Command('cancel'))
async def _cancel(message: Message, state: FSMContext):
    await message.delete()
    await state.set_state(None)
