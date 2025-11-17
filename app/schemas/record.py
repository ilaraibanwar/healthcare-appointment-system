# app/schemas/record.py
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

    model_config = {"from_attributes": True}
