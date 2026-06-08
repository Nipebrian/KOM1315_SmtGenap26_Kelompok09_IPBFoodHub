"""
Tanda tangan asimetris RSA-2048 PSS + SHA-256.
Implementasi lengkap ada di: backend/app/auth/digital_signature.py

Algoritma: RSA-2048 + PSS padding + SHA-256 (python cryptography library)
Keamanan setara: 112-bit symmetric

Fungsi:
  generate_keypair(private_path, public_path, key_size=2048) -> Tuple[str, str]
  sign_message(message, private_key_path)                    -> str (base64 signature)
  verify_signature(message, signature_b64, public_key_path)  -> bool
"""

from app.auth.digital_signature import generate_keypair, sign_message, verify_signature

__all__ = ["generate_keypair", "sign_message", "verify_signature"]
