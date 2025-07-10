from sqlalchemy import ForeignKey, String, create_engine
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
    sessionmaker,
)

engine = create_engine("sqlite:///databse.db")


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String)
    password: Mapped[str] = mapped_column(String)

    todos: Mapped["Todo"] = relationship("Todo", back_populates="user")


class Todo(Base):
    __tablename__ = "todos"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    user: Mapped["User"] = relationship("User", back_populates="todos")


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
