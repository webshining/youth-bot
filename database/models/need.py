from .base import Base


class Need(Base):
    id: str
    text: str


Need.set_collection("need")
