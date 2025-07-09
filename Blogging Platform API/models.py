import datetime
import os

from dotenv import load_dotenv
from sqlalchemy import DateTime, ForeignKey, String, create_engine, func
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
    sessionmaker,
)
from sqlalchemy.types import JSON

load_dotenv()

engine = create_engine(os.environ.get("POSTGRES_URI"), echo=True)


class Base(DeclarativeBase):
    pass


class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    content: Mapped[str] = mapped_column(String)
    categories: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    tags: Mapped[list] = mapped_column(JSON, default=list)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    category: Mapped["Category"] = relationship("Category", back_populates="posts")


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)

    posts: Mapped["Post"] = relationship("Post", back_populates="category")


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
with Session() as session:
    session.commit()
