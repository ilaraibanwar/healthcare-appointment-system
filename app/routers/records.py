# app/routers/records.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.db import models
from app.db.database import get_session
from app.schemas.record import RecordCreate, RecordOut

router = APIRouter(prefix="/records", tags=["Medical Records"])

@router.post("/", response_model=RecordOut, status_code=status.HTTP_201_CREATED)
async def create_record(payload: RecordCreate, session: AsyncSession = Depends(get_session)):
    result = await session.execute(
        select(models.Patient).where(models.Patient.id == payload.patient_id)
    )
    patient = result.scalar_one_or_none()

    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    record = models.MedicalRecord(**payload.dict())
    session.add(record)

    try:
        await session.flush()
        await session.refresh(record)
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to create record")

    return record


@router.get("/", response_model=List[RecordOut])
async def list_records(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(models.MedicalRecord))
    return result.scalars().all()


@router.get("/{record_id}", response_model=RecordOut)
async def get_record(record_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(
        select(models.MedicalRecord).where(models.MedicalRecord.id == record_id)
    )
    record = result.scalar_one_or_none()

    if not record:
        raise HTTPException(status_code=404, detail="Record not found")

    return record


@router.put("/{record_id}", response_model=RecordOut)
async def update_record(record_id: int, payload: RecordCreate, session: AsyncSession = Depends(get_session)):
    result = await session.execute(
        select(models.MedicalRecord).where(models.MedicalRecord.id == record_id)
    )
    record = result.scalar_one_or_none()

    if not record:
        raise HTTPException(status_code=404, detail="Record not found")

    for k, v in payload.dict().items():
        setattr(record, k, v)

    try:
        await session.flush()
        await session.refresh(record)
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to update record")

    return record


@router.delete("/{record_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_record(record_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(
        select(models.MedicalRecord).where(models.MedicalRecord.id == record_id)
    )
    record = result.scalar_one_or_none()

    if not record:
        raise HTTPException(status_code=404, detail="Record not found")

    try:
        await session.delete(record)
        await session.flush()
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to delete record")

    return None
