from datetime import datetime
from fastapi import APIRouter, HTTPException
from app.database.supabase_client import supabase
from app.schemas.schema import TaskCreate, TaskUpdate

router = APIRouter()
    
@router.get("/api/v1/task/get")
async def get_all_task():
    try:
        # Ambil data dari Supabase
        response = supabase.table("tasks").select("*").execute()

        return {"message": "Berhasil mengambil data", "data": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)

@router.post("/api/v1/task/create")
async def create_task(task: TaskCreate):
    try:
        # Insert data ke Supabase
        response = supabase.table("tasks").insert({
            "title": task.title,
            "description": task.description,
            "deadline": str(task.deadline),
            "status": task.status,
            "created_at": str(datetime.now()),
            "updated_at": str(datetime.now())
        }).execute()

        return {"message": "Task berhasil dibuat", "data": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)
    
@router.put("/api/v1/task/update/{task_id}")
async def update_task(task_id: int, task: TaskUpdate):
    try:
        # Konversi data ke dictionary & hilangkan nilai None
        update_data = {
                        k: (v.isoformat() if isinstance(v, datetime) else v) 
                        for k, v in task.model_dump().items() 
                        if v is not None
                    }

        # Periksa apakah ada data untuk diupdate
        if not update_data:
            raise HTTPException(status_code=400, detail="Tidak ada data yang diberikan untuk update")

        # Update task di Supabase
        response = supabase.table("tasks").update(update_data).eq("id", task_id).execute()

        # Cek apakah task ditemukan
        if not response.data:
            raise HTTPException(status_code=404, detail="Task tidak ditemukan")

        return {"message": "Task berhasil diperbarui", "data": response.data[0]}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/api/v1/task/delete/{task_id}")
async def delete_task(task_id: int):
    try:
        # Hapus task dari Supabase
        response = supabase.table("tasks").delete().eq("id", task_id).execute()

        # Cek apakah task ditemukan
        if not response.data:
            raise HTTPException(status_code=404, detail="Task tidak ditemukan")

        return {"message": "Task berhasil dihapus", "data": response.data[0]}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))