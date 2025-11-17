from .database import engine, Base
from . import models

def create_tables():
    Base.metadata.create_all(bind=engine)