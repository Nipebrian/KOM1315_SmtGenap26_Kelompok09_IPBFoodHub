# digital_signature/ — Compatibility Entrypoint

Direktori ini adalah **compatibility entrypoint** untuk modul RSA digital signature.

Implementasi lengkap ada di:
```
03_Source_Code/backend/app/auth/digital_signature.py
```

## Tentang Implementasi

- **Algoritma**: RSA-2048 PSS + SHA-256
- **Library**: Python `cryptography` (hazmat primitives)
- **Tujuan**: Non-repudiation — transaksi yang sudah ditandatangani tidak bisa
  disangkal oleh penjual maupun pembeli
- **Storage**: Signature (base64) disimpan di kolom `tanda_tangan` tabel `pesanan`

## Generate Keypair

```bash
cd 03_Source_Code/backend
python -m app.auth.digital_signature
# Output: keys/private.pem dan keys/public.pem
```

## Smoke Test

```python
from app.auth.digital_signature import sign_message, verify_signature
import json

payload = json.dumps({"pesanan_id": "abc123", "total": 50000}, sort_keys=True)
sig = sign_message(payload)
print(verify_signature(payload, sig))        # True
print(verify_signature(payload + "!", sig))  # False ← tamper detected
```
