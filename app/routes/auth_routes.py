from fastapi import APIRouter, HTTPException, Depends
from app.database.supabase_client import supabase
from app.schemas.schema import UserSignUp, UserSignIn, TokenResponse, UserResponse
from app.services.auth import get_current_user

router = APIRouter()

@router.post("/api/v1/auth/signup", response_model=UserResponse)
async def sign_up(user: UserSignUp):
    try:
        # Mendaftarkan user ke Supabase Auth dengan email
        response = supabase.auth.sign_up({
            "email": user.email,
            "password": user.password,
        })

        user_data = response.user  # Ambil data user

        # Cek apakah user sudah ada di tabel `users`
        existing_user = supabase.table("users").select("*").eq("id", user_data.id).execute()
        if existing_user.data:
            raise HTTPException(status_code=400, detail="User sudah terdaftar")

        # Simpan user ke tabel `users`
        supabase.table("users").insert({
            "id": user_data.id,
            "email": user.email,
            "username": user.username,
            "name": user.name,
        }).execute()

        return UserResponse(id=user_data.id, email=user.email, username=user.username, name=user.name)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/api/v1/auth/signin", response_model=TokenResponse)
async def sign_in(user: UserSignIn):
    try:
        # Login ke Supabase dengan email dan password
        response = supabase.auth.sign_in_with_password({
            "email": user.email,
            "password": user.password,
        })

        session = response.session  # Ambil session/token

        return {"access_token": session.access_token, "token_type": "bearer"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/api/v1/auth/me", response_model=UserResponse)
async def get_current_user_data(current_user: UserResponse = Depends(get_current_user)):
    return current_user

@router.get("/api/v1/auth/logout")
def logout():
    try:
        response = supabase.auth.sign_out()
        return {"message": "Logout berhasil"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))