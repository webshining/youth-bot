import asyncio

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.commands import set_default_commands
from app.handlers import setup_handlers
from app.middlewares import setup_middlewares
from database.models import List
from loader import bot, dp
from utils import logger


async def notify():
    users = (await List.get(1)).users
    for i in users:
        await bot.send_message(chat_id=i.user.id, text="Hello")


async def on_startup() -> None:
    await set_default_commands()
    scheduler = AsyncIOScheduler()
    # scheduler.add_job(notify, 'cron', day_of_week="mon")
    # scheduler.start()
    logger.info("Bot started!")


async def on_shutdown() -> None:
    logger.info("Bot stopped!")


async def main() -> None:
    setup_middlewares(dp)
    setup_handlers(dp)
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
