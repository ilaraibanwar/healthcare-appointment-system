# app/routers/doctors.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.db import models
from app.db.database import get_session
from app.schemas.doctor import DoctorCreate, DoctorOut

router = APIRouter(prefix="/doctors", tags=["Doctors"])

@router.post("/", response_model=DoctorOut, status_code=status.HTTP_201_CREATED)
async def create_doctor(payload: DoctorCreate, session: AsyncSession = Depends(get_session)):
    doctor = models.Doctor(**payload.dict())
    session.add(doctor)

    try:
        await session.flush()
        await session.refresh(doctor)
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to create doctor")

    return doctor


@router.get("/", response_model=List[DoctorOut])
async def list_doctors(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(models.Doctor))
    return result.scalars().all()


@router.get("/{doctor_id}", response_model=DoctorOut)
async def get_doctor(doctor_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(
        select(models.Doctor).where(models.Doctor.id == doctor_id)
    )
    doctor = result.scalar_one_or_none()

    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    return doctor


@router.put("/{doctor_id}", response_model=DoctorOut)
async def update_doctor(doctor_id: int, payload: DoctorCreate, session: AsyncSession = Depends(get_session)):
    result = await session.execute(
        select(models.Doctor).where(models.Doctor.id == doctor_id)
    )
    doctor = result.scalar_one_or_none()

    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    for k, v in payload.dict().items():
        setattr(doctor, k, v)

    try:
        await session.flush()
        await session.refresh(doctor)
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to update doctor")

    return doctor


@router.delete("/{doctor_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_doctor(doctor_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(
        select(models.Doctor).where(models.Doctor.id == doctor_id)
    )
    doctor = result.scalar_one_or_none()

    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    try:
        await session.delete(doctor)
        await session.flush()
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to delete doctor")

    return None
