import asyncio

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from app.commands import set_default_commands
from app.handlers import setup_handlers
from app.middlewares import setup_middlewares
from database.models import Config, Group
from loader import _, bot, dp
from utils import logger


async def notify():
    config = await Config.get(1)
    step = config.step
    users = (await Group.get('yyebz5ifbudmd8wq0a8t')).users
    length = len(users)
    for i, user in enumerate(users):
        next_digit = (i + step) % length
        second_user = users[next_digit].user
        try:
            await bot.send_message(chat_id=user.user.id,
                                   text=_("This week you pray for <b>{}</b>", locale=user.user.lang).format(
                                       f'<a href={f"t.me/{second_user.username}" if second_user.username else f"tg://user?id={second_user.id}"}>{second_user.name}</a>'
                                       if second_user.username else second_user.name))
        except Exception as e:
            logger.error(e)
            logger.error(f"message-{second_user.name} for {user.user.id}-{user.user.name} was not sent")
        await asyncio.sleep(0.5)
    step = 1 if step + 1 >= length else step + 1
    await Config.update(1, step=step)


async def on_startup() -> None:
    if not await Config.get(1):
        await Config.create(1)
    scheduler = AsyncIOScheduler()
    scheduler.add_job(notify, trigger=CronTrigger(day_of_week="sun", hour=20, timezone="Europe/Kyiv"))
    scheduler.start()
    await set_default_commands()
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
