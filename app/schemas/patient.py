from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class PatientBase(BaseModel):
    name: str = Field(..., max_length=256)
    age: Optional[int] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    dob: Optional[date] = None

class PatientCreate(PatientBase):
    pass

class PatientUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    dob: Optional[date] = None

class PatientOut(PatientBase):
    id: int

    class Config:
        orm_mode = True
