from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.utils.i18n import I18n
from motor.motor_tornado import MotorClient

from data.config import (I18N_DOMAIN, I18N_PATH, MONGO_URL, RD_URI,
                         TELEGRAM_BOT_TOKEN)

bot = Bot(TELEGRAM_BOT_TOKEN, parse_mode=ParseMode.HTML, disable_web_page_preview=True)
if RD_URI:
    from aiogram.fsm.storage.redis import RedisStorage
    from redis.asyncio.client import Redis

    storage = RedisStorage(Redis.from_url(RD_URI))
else:
    from aiogram.fsm.storage.memory import MemoryStorage

    storage = MemoryStorage()

dp = Dispatcher(storage=storage)
client = MotorClient(MONGO_URL)
db = client['church_youth']

i18n = I18n(path=I18N_PATH, domain=I18N_DOMAIN)
_ = i18n.gettext
