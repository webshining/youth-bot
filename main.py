import asyncio

from app.handlers import setup_handlers
from app.middlewares import setup_middlewares
from loader import bot, dp
from utils import logger


async def on_startup() -> None:
    # await set_default_commands()
    setup_middlewares(dp)
    setup_handlers(dp)
    logger.info("Bot started!")


async def on_shutdown() -> None:
    logger.info("Bot stopped!")


async def main() -> None:
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
