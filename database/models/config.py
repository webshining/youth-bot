from pydantic import Field

from loader import db
from .base import Base


class Config(Base):
    id: int = Field(default_factory=int, alias="_id")
    prayer_list: int = Field(default=1)
    step: int = Field(default=1)


Config.set_collection(db['config'])
