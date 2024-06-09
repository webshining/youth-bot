from pydantic import Field

from .base import Base


class Config(Base):
    id: str
    step: int = Field(default=1)


Config.set_collection('config')
