from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from auth.models import UserModels

engine = create_engine("sqlite:///instance.db")

UserModels.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
