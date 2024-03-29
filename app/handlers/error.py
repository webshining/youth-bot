from aiogram.types import ErrorEvent

from loader import dp
from utils import logger


@dp.errors()
async def _error(event: ErrorEvent):
    logger.error(event.exception)
