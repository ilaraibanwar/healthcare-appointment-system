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

    class Config:
        orm_mode = True
