from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import func
from app.database.supabase_client import supabase
from app.schemas.schema import TaskCreate, TaskUpdate, TaskResponse
from app.services.auth import get_current_user
from app.schemas.schema import UserResponse

router = APIRouter()

@router.get("/api/v1/task/get", response_model=list[TaskResponse])
async def get_user_task(current_user: UserResponse = Depends(get_current_user)):
    try:
        # Ambil data task hanya milik user yang sedang login
        response = supabase.table("tasks").select("*").eq("user_id", current_user.id).execute()

        if not response.data:
            return {"message": "Tidak ada task ditemukan", "data": []}

        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/api/v1/task/create", response_model=TaskResponse)
async def create_task(task: TaskCreate, current_user: UserResponse = Depends(get_current_user)):
    try:
        new_task = {
            "title": task.title,
            "description": task.description,
            "deadline": task.deadline.isoformat() if task.deadline else None,
            "status": task.status,
            "user_id": str(current_user.id),  # Tambahkan user_id dari pengguna yang sedang login
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }

        response = supabase.table("tasks").insert(new_task).execute()

        if not response.data:
            raise HTTPException(status_code=500, detail="Gagal membuat task")

        return response.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/api/v1/task/update/{task_id}", response_model=TaskResponse)
async def update_task(task_id: str, task: TaskUpdate, current_user: UserResponse = Depends(get_current_user)):
    try:
        # Konversi data ke dictionary & hilangkan nilai None
        update_data = {}
        
        for k, v in task.model_dump().items():
            if v is not None:
                if isinstance(v, datetime):
                    update_data[k] = v.isoformat()  # Ubah datetime ke ISO format
                elif isinstance(v, (str, int)):  
                    update_data[k] = v  # Biarkan str & int tetap
                else:
                    update_data[k] = str(v)  # Ubah tipe lain ke string
                    
        update_data["updated_at"] = str(func.now())

        if not update_data:
            raise HTTPException(status_code=400, detail="Tidak ada data yang diberikan untuk update")

        # Update task di Supabase dengan validasi user
        response = supabase.table("tasks").update(update_data).eq("id", task_id).eq("user_id", current_user.id).execute()

        if not response.data:
            raise HTTPException(status_code=404, detail="Task tidak ditemukan atau tidak memiliki akses")

        return response.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/api/v1/task/delete/{task_id}")
async def delete_task(task_id: str, current_user: UserResponse = Depends(get_current_user)):
    try:
        # Hapus task berdasarkan `task_id` dan `user_id`
        response = supabase.table("tasks").delete().eq("id", task_id).eq("user_id", current_user.id).execute()

        if not response.data:
            raise HTTPException(status_code=404, detail="Task tidak ditemukan atau tidak memiliki akses")

        return {"message": "Task berhasil dihapus"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
