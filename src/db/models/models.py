from datetime import datetime
from sqlalchemy import Integer, String, DateTime, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass

class TasksModel(Base):
    __tablename__ = "tasks"

    id : Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title : Mapped[str] = mapped_column(String(100), nullable=False, unique=False)
    description : Mapped[str] = mapped_column(String(300), nullable=True, unique=False)
    start_date : Mapped[datetime] = mapped_column(DateTime, nullable=False, unique=False)
    end_date : Mapped[datetime] = mapped_column(DateTime, nullable=True, unique=False)
    reward_points : Mapped[int] = mapped_column(Integer, nullable=True, unique=False)
    is_done : Mapped[bool] = mapped_column(Boolean, nullable=False, unique=False)
