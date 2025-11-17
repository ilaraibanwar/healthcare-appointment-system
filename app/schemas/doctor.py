# app/schemas/doctor.py
from pydantic import BaseModel
from datetime import datetime

class DoctorBase(BaseModel):
    name: str
    specialty: str

class DoctorCreate(DoctorBase):
    pass

class DoctorOut(DoctorBase):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}
