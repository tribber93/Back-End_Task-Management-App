from fastapi import APIRouter, HTTPException, Depends
from app.database.supabase_client import supabase, supabase_admin
from app.schemas.schema import UserSignUp, UserSignIn, TokenResponse, UserResponse
from app.services.auth import get_current_user

router = APIRouter()

@router.post("/api/v1/auth/signup", response_model=UserResponse)
async def sign_up(user: UserSignUp):
    try:
        # Cek apakah username sudah terdaftar di tabel `users`
        existing_username = supabase.table("users").select("*").eq("username", user.username).execute()
        if existing_username.data:
            raise HTTPException(status_code=400, detail="Username sudah terdaftar")

        # Cek apakah email sudah terdaftar di tabel `users`
        existing_email = supabase.table("users").select("*").eq("email", user.email).execute()
        if existing_email.data:
            raise HTTPException(status_code=400, detail="Email sudah terdaftar")
        
        # Mendaftarkan user ke Supabase Auth dengan email
        response = supabase.auth.sign_up({
            "email": user.email,
            "password": user.password,
        })

        user_data = response.user  # Ambil data user

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
    
@router.delete("/api/v1/auth/delete", response_model=dict)
async def delete_current_user(current_user: UserResponse = Depends(get_current_user)):
    try:
        user_id = current_user.id  # Ambil ID user dari current_user

        # Hapus user dari tabel `users`
        delete_response = supabase.table("users").delete().eq("id", user_id).execute()

        if not delete_response.data:
            raise HTTPException(status_code=404, detail="User tidak ditemukan di tabel `users`")

        # Hapus user dari Supabase Auth
        supabase_admin.auth.admin.delete_user(user_id)

        return {"message": "User berhasil dihapus"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))