from sqlalchemy import ForeignKey, Integer, String, create_engine, func
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
    sessionmaker,
)
from typing import List

engine = create_engine("sqlite:///instance.db")


class UserModels(DeclarativeBase):
    pass


class User(UserModels):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)