from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class PatientBase(BaseModel):
    name: str = Field(..., example="John Doe")
    age: int = Field(..., example=30)
    gender: str = Field(..., example="Male")
    contact_number: str = Field(..., example="9876543210")
    address: Optional[str] = Field(None, example="123 Health Street, Chennai")
    date_of_birth: Optional[date] = Field(None, example="1995-04-15")

class PatientCreate(PatientBase):
    pass

class PatientUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    contact_number: Optional[str] = None
    address: Optional[str] = None
    date_of_birth: Optional[date] = None

class PatientResponse(PatientBase):
    id: int

    class Config:
        orm_mode = True
