from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr
from typing import Optional
import uuid

class TaskCreate(BaseModel):
    title: str
    description: str
    deadline: datetime
    status: str  # "belum selesai", "sedang berjalan", "selesai"
    
class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    deadline: Optional[datetime] = None
    status: Optional[str] = None
    
class TaskResponse(BaseModel):
    title: str
    description: Optional[str]
    deadline: Optional[datetime]
    status: str
    user_id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Schema untuk signup
class UserSignUp(BaseModel):
    email: EmailStr  # Gunakan tipe EmailStr untuk validasi email
    username: str
    name: str
    password: str

# Schema untuk signin
class UserSignIn(BaseModel):
    email: EmailStr
    password: str

# Schema untuk response setelah signup/login
class UserResponse(BaseModel):
    id: uuid.UUID
    email: EmailStr
    username: str
    name: str

# Schema untuk token response saat login berhasil
class TokenResponse(BaseModel):
    access_token: str
    token_type: str
