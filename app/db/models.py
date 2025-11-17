from sqlalchemy import Column, Integer, String, Date, DateTime, Text, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.db.database import Base
from datetime import datetime
from app.schemas.enums import GenderEnum   # if you have this


class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256), nullable=False)
    age = Column(Integer)
    gender = Column(Enum(GenderEnum), nullable=False)
    contact_number = Column(String(15), unique=True)
    address = Column(Text)
    date_of_birth = Column(Date)
    created_at = Column(DateTime, default=datetime.utcnow)

    appointments = relationship("Appointment", back_populates="patient")

class Doctor(Base):
    __tablename__ = "doctors"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256), nullable=False)
    specialization = Column(String(256))
    contact_number = Column(String(20))
    email = Column(String(256))
    experience_years = Column(Integer)

    appointments = relationship("Appointment", back_populates="doctor")
    records = relationship("Record", back_populates="doctor")

class Appointment(Base):
    __tablename__ = "appointments"
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    doctor_id = Column(Integer, ForeignKey("doctors.id"))
    appointment_date = Column(DateTime, nullable=False)
    reason = Column(String(256))

    patient = relationship("Patient", back_populates="appointments")
    doctor = relationship("Doctor", back_populates="appointments")

class Record(Base):
    __tablename__ = "records"
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    doctor_id = Column(Integer, ForeignKey("doctors.id"))
    record_date = Column(Date, nullable=False)
    description = Column(String(512))

    patient = relationship("Patient", back_populates="appointments")
    doctor = relationship("Doctor", back_populates="records")
