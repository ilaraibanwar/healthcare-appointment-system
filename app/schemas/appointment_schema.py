from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class AppointmentBase(BaseModel):
    patient_id: int = Field(..., example=1)
    doctor_id: int = Field(..., example=2)
    appointment_date: datetime = Field(..., example="2025-11-20T10:30:00")
    reason: Optional[str] = Field(None, example="Routine check-up")

class AppointmentCreate(AppointmentBase):
    pass

class AppointmentUpdate(BaseModel):
    patient_id: Optional[int] = None
    doctor_id: Optional[int] = None
    appointment_date: Optional[datetime] = None
    reason: Optional[str] = None

class AppointmentResponse(AppointmentBase):
    id: int

    class Config:
        orm_mode = True
