from fastapi import FastAPI
from app.routers import patient_router

app = FastAPI(
    title="Healthcare Management System",
    version="1.0.0"
)

app.include_router(patient_router.router)

@app.get("/")
def root():
    return {"message": "Healthcare Management System Backend Running"}
