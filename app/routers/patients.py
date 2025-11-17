# app/routers/patients.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.db import models
from app.db.database import get_session
from app.schemas.patient import PatientCreate, PatientOut

router = APIRouter(prefix="/patients", tags=["Patients"])

@router.post("/", response_model=PatientOut, status_code=status.HTTP_201_CREATED)
async def create_patient(payload: PatientCreate, session: AsyncSession = Depends(get_session)):
    patient = models.Patient(**payload.dict())
    session.add(patient)

    try:
        await session.flush()
        await session.refresh(patient)
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to create patient")

    return patient


@router.get("/", response_model=List[PatientOut])
async def list_patients(skip: int = 0, limit: int = 100, session: AsyncSession = Depends(get_session)):
    result = await session.execute(
        select(models.Patient).offset(skip).limit(limit)
    )
    return result.scalars().all()


@router.get("/{patient_id}", response_model=PatientOut)
async def get_patient(patient_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(
        select(models.Patient).where(models.Patient.id == patient_id)
    )
    patient = result.scalar_one_or_none()

    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    return patient


@router.put("/{patient_id}", response_model=PatientOut)
async def update_patient(patient_id: int, payload: PatientCreate, session: AsyncSession = Depends(get_session)):
    result = await session.execute(
        select(models.Patient).where(models.Patient.id == patient_id)
    )
    patient = result.scalar_one_or_none()

    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    for k, v in payload.dict().items():
        setattr(patient, k, v)

    try:
        await session.flush()
        await session.refresh(patient)
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to update patient")

    return patient


@router.delete("/{patient_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_patient(patient_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(
        select(models.Patient).where(models.Patient.id == patient_id)
    )
    patient = result.scalar_one_or_none()

    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    try:
        await session.delete(patient)
        await session.flush()
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to delete patient")

    return None
