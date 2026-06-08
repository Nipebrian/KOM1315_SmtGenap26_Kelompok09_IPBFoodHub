"""
Modul database SQLAlchemy untuk IPB Food Hub.
Implementasi lengkap ada di: backend/app/core/database.py

Objek utama:
  engine       <- SQLAlchemy engine (PostgreSQL via DATABASE_URL env var)
  SessionLocal <- Session factory (autocommit=False, autoflush=False)
  Base         <- DeclarativeBase — semua model inherit dari sini
  get_db()     <- FastAPI dependency untuk mendapatkan DB session
"""

from app.core.database import engine, SessionLocal, Base, get_db

__all__ = ["engine", "SessionLocal", "Base", "get_db"]
