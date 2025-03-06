from fastapi import FastAPI
from app.routers import test_db

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Halo Duniaku"}

# Menambahkan router dari test_db.py
app.include_router(test_db.router)