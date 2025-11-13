from fastapi import APIRouter, HTTPException, status
from typing import List
from app.schemas.patient import PatientCreate, PatientOut, PatientUpdate

router = APIRouter(
    prefix="/patients",
    tags=["Patients"]
)
fake_patients_db = []

@router.post("/", response_model=PatientOut, status_code=status.HTTP_201_CREATED)
def create_patient(patient: PatientCreate):
    new_id = len(fake_patients_db) + 1
    new_patient = {"id": new_id, **patient.dict()}
    fake_patients_db.append(new_patient)
    return new_patient


@router.get("/", response_model=List[PatientOut])
def get_all_patients():
    return fake_patients_db


@router.get("/{patient_id}", response_model=PatientOut)
def get_patient(patient_id: int):
    for patient in fake_patients_db:
        if patient["id"] == patient_id:
            return patient
    raise HTTPException(status_code=404, detail="Patient not found")


@router.put("/{patient_id}", response_model=PatientOut)
def update_patient(patient_id: int, updated: PatientUpdate):
    for patient in fake_patients_db:
        if patient["id"] == patient_id:
            for key, value in updated.dict(exclude_unset=True).items():
                patient[key] = value
            return patient
    raise HTTPException(status_code=404, detail="Patient not found")


@router.delete("/{patient_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_patient(patient_id: int):
    for i, patient in enumerate(fake_patients_db):
        if patient["id"] == patient_id:
            fake_patients_db.pop(i)
            return
    raise HTTPException(status_code=404, detail="Patient not found")
