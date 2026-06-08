"""
Modul tanda tangan digital RSA-2048 PSS untuk IPB Food Hub.
Implementasi lengkap ada di: backend/app/auth/digital_signature.py

Fungsi utama:
  - generate_keypair(private_path, public_path, key_size=2048) -> Tuple[str, str]
  - sign_message(message, private_key_path)                    -> str (base64)
  - verify_signature(message, signature_b64, public_key_path)  -> bool

Cara generate keypair:
  cd backend && python -m app.auth.digital_signature

Penggunaan di routers/pesanan.py:
  payload = json.dumps({"pesanan_id": ..., "total": ..., "ts": ...}, sort_keys=True)
  signature = sign_message(payload)   # simpan ke kolom tanda_tangan
  is_valid  = verify_signature(payload, signature)  # True
"""

from app.auth.digital_signature import generate_keypair, sign_message, verify_signature

__all__ = ["generate_keypair", "sign_message", "verify_signature"]
