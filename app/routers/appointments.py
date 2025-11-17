# app/routers/appointments.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.db import models
from app.db.database import get_session
from app.schemas.appointment import AppointmentCreate, AppointmentOut

router = APIRouter(prefix="/appointments", tags=["Appointments"])

@router.post("/", response_model=AppointmentOut, status_code=status.HTTP_201_CREATED)
async def create_appointment(payload: AppointmentCreate, session: AsyncSession = Depends(get_session)):
    result_patient = await session.execute(select(models.Patient).where(models.Patient.id == payload.patient_id))
    patient = result_patient.scalar_one_or_none()

    result_doctor = await session.execute(select(models.Doctor).where(models.Doctor.id == payload.doctor_id))
    doctor = result_doctor.scalar_one_or_none()

    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    appointment = models.Appointment(**payload.dict())
    session.add(appointment)

    try:
        await session.flush()
        await session.refresh(appointment)
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to create appointment")

    return appointment


@router.get("/", response_model=List[AppointmentOut])
async def list_appointments(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(models.Appointment))
    return result.scalars().all()


@router.get("/{appointment_id}", response_model=AppointmentOut)
async def get_appointment(appointment_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(
        select(models.Appointment).where(models.Appointment.id == appointment_id)
    )
    appointment = result.scalar_one_or_none()

    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")

    return appointment


@router.put("/{appointment_id}", response_model=AppointmentOut)
async def update_appointment(appointment_id: int, payload: AppointmentCreate, session: AsyncSession = Depends(get_session)):
    result = await session.execute(
        select(models.Appointment).where(models.Appointment.id == appointment_id)
    )
    appointment = result.scalar_one_or_none()

    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")

    for k, v in payload.dict().items():
        setattr(appointment, k, v)

    try:
        await session.flush()
        await session.refresh(appointment)
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to update appointment")

    return appointment


@router.delete("/{appointment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_appointment(appointment_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(
        select(models.Appointment).where(models.Appointment.id == appointment_id)
    )
    appointment = result.scalar_one_or_none()

    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")

    try:
        await session.delete(appointment)
        await session.flush()
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to delete appointment")

    return None
