"""
Unit test RSA-2048 PSS + SHA-256 digital signature.
Modul: app.auth.digital_signature
"""
import os
import json
import pytest
from app.auth.digital_signature import generate_keypair, sign_message, verify_signature


@pytest.fixture(scope="module")
def keypair(tmp_path_factory):
    d = tmp_path_factory.mktemp("keys")
    priv = str(d / "private.pem")
    pub  = str(d / "public.pem")
    generate_keypair(priv, pub)
    return priv, pub


@pytest.fixture(scope="module")
def sample_payload():
    return json.dumps(
        {"pesanan_id": "abc-123", "total_harga": 50000, "ts": "2026-06-05T09:00:00Z"},
        sort_keys=True
    )


class TestDigitalSignature:

    def test_generate_keypair(self, keypair):
        priv, pub = keypair
        assert os.path.exists(priv), "private.pem harus terbuat"
        assert os.path.exists(pub),  "public.pem harus terbuat"
        assert os.path.getsize(priv) > 0
        assert os.path.getsize(pub)  > 0

    def test_sign_and_verify_valid(self, keypair, sample_payload):
        priv, pub = keypair
        sig = sign_message(sample_payload, priv)
        assert isinstance(sig, str) and len(sig) > 0
        assert verify_signature(sample_payload, sig, pub) is True

    def test_tampered_payload_rejected(self, keypair, sample_payload):
        priv, pub = keypair
        sig = sign_message(sample_payload, priv)
        tampered = sample_payload + "!"
        assert verify_signature(tampered, sig, pub) is False

    def test_forged_signature_rejected(self, keypair, sample_payload):
        _, pub = keypair
        # Signature yang bukan hasil sign_message
        assert verify_signature(sample_payload, "aW52YWxpZHNpZ25hdHVyZQ==", pub) is False

    def test_empty_signature_rejected(self, keypair, sample_payload):
        _, pub = keypair
        assert verify_signature(sample_payload, "", pub) is False

    def test_different_payloads_different_signatures(self, keypair):
        priv, pub = keypair
        msg1 = json.dumps({"pesanan_id": "abc", "total": 50000}, sort_keys=True)
        msg2 = json.dumps({"pesanan_id": "xyz", "total": 99000}, sort_keys=True)
        assert sign_message(msg1, priv) != sign_message(msg2, priv)
