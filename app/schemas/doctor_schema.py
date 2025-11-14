from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class DoctorBase(BaseModel):
    name: str = Field(..., example="Dr. Priya Sharma")
    specialization: str = Field(..., example="Cardiology")
    contact_number: str = Field(..., example="9876543210")
    email: Optional[EmailStr] = Field(None, example="priya.sharma@hospital.com")
    experience_years: Optional[int] = Field(None, example=10)

class DoctorCreate(DoctorBase):
    pass

class DoctorUpdate(BaseModel):
    name: Optional[str] = None
    specialization: Optional[str] = None
    contact_number: Optional[str] = None
    email: Optional[EmailStr] = None
    experience_years: Optional[int] = None

class DoctorResponse(DoctorBase):
    id: int

    class Config:
        orm_mode = True
