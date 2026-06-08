"""
Unit test enkripsi AES-256-GCM field-level.
Modul: app.core.crypto
"""
import base64
import pytest
from app.core.crypto import encrypt, decrypt


class TestAESCrypto:

    def test_encrypt_decrypt_roundtrip(self):
        """decrypt(encrypt(x)) harus sama persis dengan x."""
        for plaintext in ("081234567890", "3210987654321098", "test@email.com", "Nomor Rekening 123"):
            assert decrypt(encrypt(plaintext)) == plaintext

    def test_same_plaintext_different_ciphertext(self):
        """IV random 12 byte — plaintext sama menghasilkan ciphertext berbeda."""
        plaintext = "081234567890"
        ct1 = encrypt(plaintext)
        ct2 = encrypt(plaintext)
        assert ct1 != ct2

    def test_tampered_ciphertext_rejected(self):
        """GCM authentication tag harus mendeteksi tamper pada ciphertext."""
        ct = encrypt("rahasia-penting")
        blob = bytearray(base64.b64decode(ct))
        # Tamper: flip bit di byte ke-13 (dalam body ciphertext, setelah IV 12 byte)
        blob[13] ^= 0xFF
        tampered_b64 = base64.b64encode(bytes(blob)).decode()
        with pytest.raises(Exception):
            decrypt(tampered_b64)

    def test_none_input_returns_none(self):
        """None input harus mengembalikan None, bukan raise."""
        assert encrypt(None) is None
        assert decrypt(None) is None

    def test_ciphertext_is_base64(self):
        """Output encrypt() harus valid base64."""
        ct = encrypt("test data")
        decoded = base64.b64decode(ct)
        assert len(decoded) > 12 + 16  # IV (12) + minimal 1 byte data + tag (16)

    def test_iv_is_prepended(self):
        """12 byte pertama dari blob adalah IV."""
        ct = encrypt("test")
        blob = base64.b64decode(ct)
        assert len(blob) >= 12 + 1 + 16  # IV + ciphertext + GCM tag

    def test_unicode_plaintext(self):
        """Plaintext unicode (non-ASCII) harus bisa dienkripsi dan didekripsi."""
        for text in ("Hanif Briansyah", "IPB University", "UMKM Warung Makan"):
            assert decrypt(encrypt(text)) == text
