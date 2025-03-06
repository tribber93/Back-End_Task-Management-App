from fastapi import APIRouter
from app.database.supabase_client import supabase

router = APIRouter()

@router.get("/test-db")
async def test_db():
    """
    Test the connection to the database
    """
    try:
        response = supabase.table("test").select("*").execute()
    except Exception as e:
        return {"message": e}
    return {"message": response}
        
@router.post("/test-db")
async def test_db_post(name: str):
    response = supabase.table("test").insert({"name": name}).execute()
    return {"message": response}

@router.delete("/test-db")
async def test_db_delete(id: int):
    response = supabase.table("test").delete().eq("id", id).execute()
    return {"message": response}