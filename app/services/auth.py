from fastapi import Depends, HTTPException, Security
from fastapi.security import OAuth2PasswordBearer, HTTPAuthorizationCredentials, HTTPBearer
from app.database.supabase_client import supabase
from app.schemas.schema import UserResponse

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/signin")
oauth2_scheme = HTTPBearer()


async def get_current_user(credentials: HTTPAuthorizationCredentials = Security(oauth2_scheme)) -> UserResponse:
    try:
        token = credentials.credentials  # Ambil string token dari HTTPBearer
        # print(f"Token yang diterima: {token}")

        # Verifikasi token dengan Supabase
        response = supabase.auth.get_user(token)
        # print(response)

        user_data = response.user
        # Ambil data tambahan dari tabel `users`
        user_info = (
            supabase.table("users")
            .select("id, email, username, name")
            .eq("id", user_data.id)
            .single()
            .execute()
        )

        if not user_info or not user_info.data:
            raise HTTPException(status_code=401, detail="User tidak ditemukan")

        return UserResponse(**user_info.data)

    except HTTPException as e:
        raise e  # Jika error sudah HTTPException, langsung lempar
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Terjadi kesalahan: {str(e)}")