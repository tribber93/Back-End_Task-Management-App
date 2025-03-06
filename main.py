import uvicorn
from fastapi import FastAPI
from app.routers import task_router

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Halo Everybody!"}

# Menambahkan router dari test_db.py
app.include_router(task_router.router)

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True, log_level="debug")