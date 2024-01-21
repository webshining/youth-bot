from sqlalchemy import BigInteger, Integer, String, select, Table, ForeignKey, Column
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.models.base import BaseModel

association_table = Table(
    "list_user",
    BaseModel.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("list_id", ForeignKey("lists.id"), primary_key=True),
)


class User(BaseModel):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    username: Mapped[str] = mapped_column(String, nullable=True)
    status: Mapped[str] = mapped_column(String, default="user")
    lists: Mapped[list["List"]] = relationship(secondary=association_table, back_populates="users")

    @classmethod
    async def get_or_create(cls, session: AsyncSession, id: int, name: str, username: str = None):
        stmt = select(cls).where(cls.id == id)
        obj = await session.scalar(stmt)
        if not obj:
            obj = cls(id=id, name=name, username=username)
            session.add(obj)
            await session.flush()
        session.expunge_all()
        return obj


class List(BaseModel):
    __tablename__ = "lists"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    users: Mapped[list["User"]] = relationship(secondary=association_table, back_populates="lists", lazy="selectin")
