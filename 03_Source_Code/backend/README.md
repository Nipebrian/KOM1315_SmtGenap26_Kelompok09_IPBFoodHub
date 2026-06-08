# Backend — IPB Food Hub & UMKM

Kode FastAPI (Python) untuk sistem pemesanan makanan kampus IPB dengan implementasi
keamanan informasi (AAA, enkripsi AES-256-GCM, tanda tangan digital RSA-2048 PSS).

Struktur folder (implementasi sudah tersedia):

```
backend/
├── app/
│   ├── main.py                    ← Entry point FastAPI, middleware audit log
│   ├── auth/
│   │   └── digital_signature.py   ← RSA-2048 PSS sign/verify (NON-REPUDIATION)
│   ├── core/
│   │   ├── config.py              ← Env vars (SECRET_KEY, ENCRYPTION_KEY, dll)
│   │   ├── crypto.py              ← AES-256-GCM encrypt/decrypt
│   │   ├── database.py            ← SQLAlchemy engine & session
│   │   ├── logging_aaa.py         ← AAA audit log (JSON Lines ke file)
│   │   └── security.py            ← JWT create/verify, bcrypt, RBAC require_role()
│   ├── models/
│   │   ├── audit_log.py           ← Tabel audit_logs (API request log)
│   │   ├── user.py                ← Tabel users
│   │   └── ...
│   ├── routers/
│   │   ├── auth.py                ← POST /api/auth/login, /register, GET /api/auth/me
│   │   ├── security.py            ← GET /api/security/audit-logs (dashboard admin)
│   │   └── ...
│   └── schemas/
│       └── ...
├── tests/
│   ├── test_digital_signature.py  ← Unit test RSA signature
│   ├── test_security.py           ← Unit test JWT guard & RBAC
│   └── test_crypto.py             ← Unit test AES enkripsi
├── .env.example
├── requirements.txt
└── vercel.json
```

## Cara Menjalankan

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```
