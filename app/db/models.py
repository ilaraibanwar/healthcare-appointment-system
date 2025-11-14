from sqlalchemy import Column, Integer, String, Date
from app.db.database import Base

class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256), nullable=False)
    age = Column(Integer)
    email = Column(String(256))
    phone = Column(String(20))
    dob = Column(Date)
