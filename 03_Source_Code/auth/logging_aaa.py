"""
Modul Accounting (AAA) — audit log untuk IPB Food Hub.
Implementasi lengkap ada di: backend/app/core/logging_aaa.py

Fungsi utama:
  - log_accounting(user_id, action, details, ip)  -> None
  - log_login_attempt(email, success, ip, reason) -> None

Event yang dicatat:
  LOGIN_SUCCESS, LOGIN_FAILED, USER_REGISTER,
  ACCESS_GRANTED, ACCESS_DENIED, PROFILE_UPDATE

Format output (JSON Lines):
  {"ts": "...", "user_id": "...", "action": "LOGIN_SUCCESS",
   "details": "role=mahasiswa", "ip": "127.0.0.1"}
"""

from app.core.logging_aaa import log_accounting, log_login_attempt

__all__ = ["log_accounting", "log_login_attempt"]
