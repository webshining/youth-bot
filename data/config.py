from pathlib import Path

from environs import Env

env = Env()
env.read_env()

DIR = Path(__file__).absolute().parent.parent

TELEGRAM_BOT_TOKEN = env.str("TELEGRAM_BOT_TOKEN")

SURREAL_URL = env.str("SURREAL_URL", "ws://localhost:8000/rpc")
SURREAL_NS = env.str("SURREAL_NS", "test")
SURREAL_DB = env.str("SURREAL_DB", "test")
SURREAL_USER = env.str("SURREAL_USER", None)
SURREAL_PASS = env.str("SURREAL_PASS", None)


RD_DB = env.int("RD_DB", 5)
RD_HOST = env.str("RD_HOST", "localhost")
RD_PORT = env.int("RD_PORT", 6379)

RD_URI = env.str("RD_URI", default=f"redis://{RD_HOST}:{RD_PORT}/{RD_DB}")

I18N_PATH = f"{DIR}/data/locales"
I18N_DOMAIN = env.str("I18N_DOMAIN", "bot")

DOMAIN = env.str("DOMAIN", "127.0.0.1")
FRONTEND_URL = env.str("FRONTEND_URL", "http://127.0.0.1:3000")
ACCESS_TOKEN_SECRET_KEY = env.str("ACCESS_TOKEN_SECRET_KEY", "accesssecretkey")
ACCESS_TOKEN_EXPIRE_MINUTES = env.int("ACCESS_TOKEN_EXPIRE_MINUTES", 1)
REFRESH_TOKEN_SECRET_KEY = env.str("REFRESH_TOKEN_SECRET_KEY", "refreshsecretkey")
REFRESH_TOKEN_EXPIRE_MINUTES = env.int("REFRESH_TOKEN_EXPIRE_MINUTES", 60 * 24 * 30)
