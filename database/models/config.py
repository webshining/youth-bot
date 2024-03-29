from pydantic import Field

from .base import Base


class Config(Base):
    id: int = Field(default_factory=int, alias="_id")
    step: int = Field(default=1)


Config.set_collection('config')
