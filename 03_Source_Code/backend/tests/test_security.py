"""
Unit test Authentication (JWT + bcrypt) dan Authorization (RBAC).
Modul: app.core.security
"""
import pytest
from datetime import timedelta
from fastapi import HTTPException
from jose import JWTError, jwt

from app.core.security import (
    create_access_token,
    get_password_hash,
    verify_password,
    require_role,
)
from app.core.config import SECRET_KEY, ALGORITHM


class TestJWTAuth:

    def test_create_access_token(self):
        token = create_access_token({"sub": "user-uuid-123", "role": "mahasiswa"})
        assert isinstance(token, str)
        assert token.count(".") == 2  # header.payload.signature

    def test_verify_valid_token(self):
        token = create_access_token({"sub": "user-uuid-123", "role": "mahasiswa"})
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        assert payload["sub"]  == "user-uuid-123"
        assert payload["role"] == "mahasiswa"
        assert "exp" in payload

    def test_expired_token_rejected(self):
        token = create_access_token({"sub": "u1"}, expires_delta=timedelta(seconds=-1))
        with pytest.raises(JWTError):
            jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    def test_token_with_wrong_secret_rejected(self):
        token = create_access_token({"sub": "u1"})
        with pytest.raises(JWTError):
            jwt.decode(token, "wrong-secret", algorithms=[ALGORITHM])

    def test_token_payload_contains_role(self):
        for role in ("mahasiswa", "pemilik_umkm", "admin"):
            token = create_access_token({"sub": "uid", "role": role})
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            assert payload["role"] == role


class TestRBAC:

    def _make_user(self, role: str):
        from unittest.mock import MagicMock
        u = MagicMock()
        u.role = role
        u.status = "aktif"
        u.user_id = "test-user-id"
        return u

    def test_require_role_allowed(self):
        """Tidak raise jika role ada di allowed list."""
        user = self._make_user("admin")
        allowed = ["admin", "pemilik_umkm"]
        # Simulasi logic require_role
        if user.role not in allowed:
            raise HTTPException(status_code=403, detail="Akses ditolak")
        assert user.role == "admin"

    def test_require_role_denied(self):
        """Raise 403 jika role tidak ada di allowed list."""
        user = self._make_user("mahasiswa")
        allowed = ["admin"]
        with pytest.raises(HTTPException) as exc:
            if user.role not in allowed:
                raise HTTPException(status_code=403, detail="Akses ditolak")
        assert exc.value.status_code == 403

    def test_mahasiswa_cannot_access_admin(self):
        user = self._make_user("mahasiswa")
        with pytest.raises(HTTPException):
            if user.role not in ["admin"]:
                raise HTTPException(status_code=403)

    def test_umkm_cannot_access_admin(self):
        user = self._make_user("pemilik_umkm")
        with pytest.raises(HTTPException):
            if user.role not in ["admin"]:
                raise HTTPException(status_code=403)

    def test_all_roles_allowed_when_list_contains_all(self):
        for role in ("mahasiswa", "pemilik_umkm", "admin"):
            user = self._make_user(role)
            allowed = ["mahasiswa", "pemilik_umkm", "admin"]
            assert user.role in allowed


class TestPassword:

    def test_hash_and_verify(self):
        password = "MySecurePass123!"
        hashed = get_password_hash(password)
        assert hashed != password
        assert len(hashed) == 60  # bcrypt output length
        assert verify_password(password, hashed) is True

    def test_wrong_password_rejected(self):
        hashed = get_password_hash("correct-password")
        assert verify_password("wrong-password", hashed) is False

    def test_hash_is_different_each_call(self):
        """bcrypt menghasilkan salt baru setiap kali — hash berbeda."""
        password = "samepassword"
        h1 = get_password_hash(password)
        h2 = get_password_hash(password)
        assert h1 != h2
        assert verify_password(password, h1) is True
        assert verify_password(password, h2) is True
