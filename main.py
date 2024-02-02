import asyncio
import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from app.commands import set_default_commands
from app.handlers import setup_handlers
from app.middlewares import setup_middlewares
from database.models import Config, List
from loader import _, bot, dp
from utils import logger

logging.basicConfig(level=logging.WARNING)


async def notify():
    config = await Config.get(1)
    step = config.step
    users = (await List.get(1)).users
    length = len(users)
    for i in range(1, length + 1):
        next_digit = (i + step - 1) % length + 1
        first_user = users[i - 1].user
        second_user = users[next_digit - 1].user
        try:
            await bot.send_message(chat_id=first_user.id,
                                   text=_("This week you pray for <b>{}</b>", locale=first_user.lang).format(
                                       f'<a href="t.me/{second_user.username}">{second_user.name}</a>'
                                       if second_user.username else second_user.name))
        except Exception as e:
            logger.error(e)
            logger.error(f"message-{second_user.name} for {first_user.id}-{first_user.name} was not sent")
        await asyncio.sleep(0.5)
    step = 1 if step + 1 >= length else step + 1
    await Config.update(1, step=step)


async def on_startup() -> None:
    if not await Config.get(1):
        await Config.create()
    await set_default_commands()
    scheduler = AsyncIOScheduler()
    scheduler.add_job(notify, trigger=CronTrigger(day_of_week="sun", hour=20, timezone="Europe/Kyiv"))
    scheduler.start()
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
