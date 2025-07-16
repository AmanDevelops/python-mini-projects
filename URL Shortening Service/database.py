from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

engine = create_engine("sqlite:///instance.db")


class Base(DeclarativeBase):
    pass


Session = sessionmaker(bind=engine)

def init_db():
    """Initialize database tables - import models here to avoid circular imports"""
    from auth.models import User
    from service.models import Urls
    
    Base.metadata.create_all(engine)