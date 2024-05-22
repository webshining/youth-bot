import urllib.parse
from pathlib import Path

from environs import Env

env = Env()
env.read_env()

DIR = Path(__file__).absolute().parent.parent

TELEGRAM_BOT_TOKEN = env.str('TELEGRAM_BOT_TOKEN')

MONGO_HOST = env.str("MONGO_HOST", "localhost")
MONGO_PORT = env.int("MONGO_PORT", 27017)
MONGO_USER = env.str("MONGO_USER", None)
MONGO_PASS = env.str("MONGO_PASS", None)

MONGO_URL = env.str('MONGO_URL', f"mongodb://{MONGO_HOST}:{MONGO_PORT}/")
if MONGO_PASS and MONGO_USER:
    MONGO_URL = f'mongodb://{urllib.parse.quote(MONGO_USER)}:{urllib.parse.quote(MONGO_PASS)}@{MONGO_HOST}:{MONGO_PORT}'

RD_DB = env.int('RD_DB', 5)
RD_HOST = env.str('RD_HOST', "localhost")
RD_PORT = env.int('RD_PORT', 6379)

RD_URI = env.str('RD_URI', default=f"redis://{RD_HOST}:{RD_PORT}/{RD_DB}")

FRONTEND_URL = env.str('FRONTEND_URL', 'http://localhost:3000')
ACCESS_TOKEN_SECRET_KEY = env.str('ACCESS_TOKEN_SECRET_KEY', 'accesssecretkey')
ACCESS_TOKEN_EXPIRE_MINUTES = env.int('ACCESS_TOKEN_EXPIRE_MINUTES', 2)
REFRESH_TOKEN_SECRET_KEY = env.str('REFRESH_TOKEN_SECRET_KEY', 'refreshsecretkey')
REFRESH_TOKEN_EXPIRE_MINUTES = env.int('REFRESH_TOKEN_EXPIRE_MINUTES', 60 * 24 * 30)

I18N_PATH = f'{DIR}/data/locales'
I18N_DOMAIN = env.str('I18N_DOMAIN', 'bot')
