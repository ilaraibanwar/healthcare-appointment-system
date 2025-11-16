from pydantic import BaseModel
from datetime import datetime

class RecordBase(BaseModel):
    patient_id: int
    diagnosis: str
    treatment: str

class RecordCreate(RecordBase):
    pass

class RecordOut(RecordBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
