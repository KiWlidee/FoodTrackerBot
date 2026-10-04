from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, Float

from database import Base


class Purpose(Base):
    __tablename__ = "purpose_tracking"

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(Integer())
    water_ml: Mapped[int] = mapped_column(Integer(), default=0)
    calories: Mapped[float] = mapped_column(Float(), default=0)
    protein: Mapped[float] = mapped_column(Float(), default=0)
    fat: Mapped[float] = mapped_column(Float(), default=0)
    carbs: Mapped[float] = mapped_column(Float(), default=0)