from sqlalchemy import UUID, Column, ForeignKey, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from app.database.session import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)  # Judul tugas
    description = Column(Text, nullable=True)  # Deskripsi tugas
    deadline = Column(DateTime, nullable=True)  # Tanggal deadline
    status = Column(String(20), default="belum selesai")  # Status tugas
    
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())  # Update otomatis
