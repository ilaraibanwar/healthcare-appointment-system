from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class RecordBase(BaseModel):
    patient_id: int = Field(..., example=1)
    doctor_id: int = Field(..., example=2)
    record_date: date = Field(..., example="2025-11-14")
    description: Optional[str] = Field(None, example="Patient reported mild fever and cough.")

class RecordCreate(RecordBase):
    pass

class RecordUpdate(BaseModel):
    patient_id: Optional[int] = None
    doctor_id: Optional[int] = None
    record_date: Optional[date] = None
    description: Optional[str] = None

class RecordResponse(RecordBase):
    id: int

    class Config:
        orm_mode = True
