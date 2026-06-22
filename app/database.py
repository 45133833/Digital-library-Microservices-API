from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy import event
import os

from pydantic_settings import BaseSettings

# ✨ تعريف الكلاس فقط (بدون إنشاء instance داخله)
class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/library"


DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/library")


settings = Settings()

engine = create_engine(
    DATABASE_URL,
    echo=True,  # Log SQL queries
    client_encoding="utf8"
)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
        
        
