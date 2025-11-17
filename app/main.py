# app/main.py
from fastapi import FastAPI
from dotenv import load_dotenv
import asyncio

from app.db.database import create_tables
from app.routers import patients, doctors, appointments, records

load_dotenv()

app = FastAPI(title="Healthcare Management API", version="1.0.0")

@app.on_event("startup")
async def startup_event():
    try:
        await create_tables()
    except Exception:
        raise RuntimeError("Failed to initialize database tables.")

app.include_router(patients.router)
app.include_router(doctors.router)
app.include_router(appointments.router)
app.include_router(records.router)

@app.get("/")
async def health():
    return {"status": "ok"}
