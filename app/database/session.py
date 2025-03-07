import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

username = os.environ.get("SUPABASE_USER")
password = os.environ.get("SUPABASE_PASSWORD")
host = os.environ.get("SUPABASE_HOST")
port = os.environ.get("SUPABASE_PORT")
database = os.environ.get("SUPABASE_DATABASE")

DATABASE_URL = f"postgresql://{username}:{password}@{host}:{port}/{database}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
