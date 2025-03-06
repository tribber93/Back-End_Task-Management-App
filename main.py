import uvicorn
from fastapi import FastAPI
from app.routes import task_routes, auth_routes

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Halo Everybody!"}

# Menambahkan router dari test_db.py
app.include_router(task_routes.router)
app.include_router(auth_routes.router)

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True, log_level="debug")