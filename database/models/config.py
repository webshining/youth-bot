from pydantic import Field

from loader import db

from .base import Base


class Config(Base):
    id: int = Field(default_factory=int, alias="_id")
    prayer_list: int = Field(default=1)
    cron_hour: int = Field(default=18)
    cron_weekday: str = Field(default="sun")
    step: int = Field(default=1)


Config.set_collection(db['config'])
