from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()

from app.db import models
from app.db.database import engine
from app.routers import patients, doctors, appointments, records

# Auto-create tables in dev (remove in production)
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Healthcare Management API", version="1.0.0")

# Register routers
app.include_router(patients.router)
app.include_router(doctors.router)
app.include_router(appointments.router)
app.include_router(records.router)

@app.get("/")
def health():
    return {"status": "ok"}
