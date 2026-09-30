from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer

from database import Base


class UsersOrm(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(Integer(), unique=True)
    username: Mapped[str | None] = mapped_column(String(50), nullable=True)