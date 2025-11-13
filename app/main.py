from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Healthcare Management System Backend Running"}
