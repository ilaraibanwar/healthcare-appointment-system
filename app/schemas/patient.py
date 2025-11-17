# app/schemas/patient.py
from pydantic import BaseModel
from datetime import datetime

class PatientBase(BaseModel):
    name: str
    age: int
    gender: str | None = None

class PatientCreate(PatientBase):
    pass

class PatientOut(PatientBase):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}
