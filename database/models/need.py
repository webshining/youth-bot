from pydantic import Field

from .base import Base


class Need(Base):
    id: int = Field(default_factory=int, alias="_id")
    text: str


Need.set_collection("needs")
