from pydantic import BaseModel
from datetime import datetime

class AppointmentBase(BaseModel):
    patient_id: int
    doctor_id: int
    date: datetime
    reason: str | None = None

class AppointmentCreate(AppointmentBase):
    pass

class AppointmentOut(AppointmentBase):
    id: int
    status: str
    created_at: datetime

    class Config:
        orm_mode = True
