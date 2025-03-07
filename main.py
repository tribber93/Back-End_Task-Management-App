import uvicorn
from fastapi import FastAPI
from app.routes import task_routes, auth_routes
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Halo Everybody!"}

# Menambahkan router dari test_db.py
app.include_router(task_routes.router)
app.include_router(auth_routes.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Bisa diganti dengan domain frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, log_level="debug")