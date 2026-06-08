"""
Modul keamanan Authentication + Authorization (RBAC) untuk IPB Food Hub.
Implementasi lengkap ada di: backend/app/core/security.py

Fungsi utama:
  - create_access_token(data, expires_delta)  -> str (JWT HS256)
  - verify_password(plain, hashed)            -> bool (bcrypt)
  - get_password_hash(password)               -> str (bcrypt hash)
  - get_current_user(token, db)               -> User (FastAPI Depends)
  - require_role(allowed_roles)               -> Callable (FastAPI Depends)

Catatan keamanan:
  - JWT menggunakan algoritma HS256 dengan SECRET_KEY dari env
  - Password di-hash dengan bcrypt (work factor default: 12)
  - Setiap akses melalui get_current_user() dicatat ke AAA audit log
  - require_role() mengembalikan 403 Forbidden jika role tidak sesuai
"""

from app.core.security import (
    create_access_token,
    verify_password,
    get_password_hash,
    get_current_user,
    require_role,
    oauth2_scheme,
)

__all__ = [
    "create_access_token",
    "verify_password",
    "get_password_hash",
    "get_current_user",
    "require_role",
    "oauth2_scheme",
]
