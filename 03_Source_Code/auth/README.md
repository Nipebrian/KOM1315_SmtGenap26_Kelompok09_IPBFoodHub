# auth/ — Compatibility Entrypoint

Direktori ini adalah **compatibility entrypoint** untuk struktur kursus KOM1315
yang mengharapkan adanya folder `auth/` di level `03_Source_Code/`.

Implementasi autentikasi yang sebenarnya ada di:
```
03_Source_Code/backend/app/core/security.py     ← JWT, bcrypt, RBAC
03_Source_Code/backend/app/routers/auth.py      ← Endpoint /api/auth/*
03_Source_Code/backend/app/auth/digital_signature.py ← RSA digital signature
```

Setiap file di sini me-re-import fungsi utama dari modul backend di atas,
sehingga dokumentasi dan referensi kode dapat langsung menunjuk ke folder ini.

## Modul yang Di-re-export

| File | Re-export dari |
|------|---------------|
| `security.py` | `backend/app/core/security.py` |
| `digital_signature.py` | `backend/app/auth/digital_signature.py` |
| `logging_aaa.py` | `backend/app/core/logging_aaa.py` |
