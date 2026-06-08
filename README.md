# IPB Food Hub & UMKM — Keamanan Informasi (KOM1315)

Platform marketplace digital untuk UMKM dan mahasiswa IPB University. Repository ini
berfokus pada implementasi modul keamanan informasi yang mencakup autentikasi, otorisasi,
enkripsi data, tanda tangan digital, dan audit log.

## Tech Stack

### Backend
- **Framework**: FastAPI (Python 3.12)
- **Database**: PostgreSQL via SQLAlchemy ORM
- **Auth**: JWT (python-jose) + bcrypt password hashing
- **Enkripsi**: AES-256-GCM (library `cryptography`)
- **Digital Signature**: RSA-2048 PSS + SHA-256 (library `cryptography`)
- **Deployment**: Vercel Serverless

### Frontend
- **Framework**: React 18 + Vite
- **Styling**: CSS Modules
- **Language**: JavaScript (JSX)

## Repository Structure

| Folder | Isi |
|--------|-----|
| `01_Proposal_&_Analisis/` | Proposal teknis & threat modeling |
| `02_Design_Documents/` | Architecture diagram, ERD, testing plan |
| `03_Source_Code/` | Source code backend (FastAPI) & frontend (React) |
| `04_Reports_&_Paper/` | Laporan akhir, monitoring P7, scientific paper |
| `05_Testing/` | Log hasil unit test & audit |


### Repository Structure Note

Folder `03_Source_Code/auth/`, `03_Source_Code/digital_signature/`, dan
`03_Source_Code/database/` adalah **compatibility entrypoint** yang me-re-export
implementasi asli dari `03_Source_Code/backend/app/`. Pola ini digunakan agar
struktur repo sesuai dengan yang diharapkan kursus tanpa refaktor besar-besaran.

---

## Prerequisites

- Python >= 3.12
- PostgreSQL database
- Node.js >= 18 (untuk frontend)
- pip / venv

---

## Installation

### Backend
```bash
cd 03_Source_Code/backend
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Linux/Mac
pip install -r requirements.txt
```

### Frontend
```bash
cd 03_Source_Code/frontend
npm install
```

---

## Environment Variables

Buat file `03_Source_Code/backend/.env` dari template `.env.example`.

```env
DATABASE_URL=postgresql://user:password@localhost/ipb_food_hub
SECRET_KEY=your_jwt_secret_key_min_32_chars
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# AES-256-GCM (32 byte, base64-encoded)
ENCRYPTION_KEY=your_base64_32byte_key

# RSA key paths (auto-generate via: python -m app.auth.digital_signature)
RSA_PRIVATE_KEY_PATH=./keys/private.pem
RSA_PUBLIC_KEY_PATH=./keys/public.pem

# Cloudinary (opsional, untuk upload gambar)
CLOUDINARY_CLOUD_NAME=
CLOUDINARY_API_KEY=
CLOUDINARY_API_SECRET=

# CORS — daftar origin frontend yang diizinkan (pisahkan dengan koma)
ALLOWED_ORIGINS=http://localhost:5173,https://ipb-food-hub.vercel.app

# AAA Audit Log — opsional, default ./logs/aaa_accounting.log
# AAA_LOG_DIR=/custom/log/path
```

Generate `SECRET_KEY`:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Generate `ENCRYPTION_KEY`:
```bash
python -c "import os, base64; print(base64.b64encode(os.urandom(32)).decode())"
```

Generate RSA keypair:
```bash
cd 03_Source_Code/backend
python -m app.auth.digital_signature
```

---

## Running the App

### Backend
```bash
cd 03_Source_Code/backend
uvicorn app.main:app --reload --port 8000
```

### Frontend
```bash
cd 03_Source_Code/frontend
npm run dev
```

---

## Database

```bash
cd 03_Source_Code/backend
# Tabel dibuat otomatis oleh SQLAlchemy saat pertama kali run
# Atau jalankan script inisialisasi:
python -c "from app.core.database import Base, engine; Base.metadata.create_all(bind=engine)"
```

---

## Testing

```bash
cd 03_Source_Code/backend
pytest tests/ -v
# Simpan output ke 05_Testing/unit-test-security.log:
pytest tests/ -v 2>&1 | tee ../../05_Testing/unit-test-security.log
```

---

## Available Scripts (Backend)

| Script | Deskripsi |
|--------|-----------|
| `uvicorn app.main:app --reload` | Development mode (auto-reload) |
| `python -m app.auth.digital_signature` | Generate RSA keypair |
| `pytest tests/ -v` | Jalankan semua unit test |

## Fitur Keamanan yang Diimplementasikan

| No | Fitur | Implementasi |
|----|-------|-------------|
| 1 | JWT Authentication | `app/core/security.py` — `create_access_token()`, `get_current_user()` |
| 2 | RBAC | `app/core/security.py` — `require_role()` decorator |
| 3 | AES-256-GCM Enkripsi | `app/core/crypto.py` — `encrypt()`, `decrypt()` |
| 4 | RSA-2048 Digital Signature | `app/auth/digital_signature.py` — `sign_message()`, `verify_signature()` |
| 5 | bcrypt Password Hashing | `app/core/security.py` — `get_password_hash()`, `verify_password()` |
| 6 | AAA Audit Log | `app/core/logging_aaa.py` — `log_accounting()`, `log_login_attempt()` |
| 7 | API Request Audit Log | `app/models/audit_log.py` + middleware di `app/main.py` |
| 8 | Security Dashboard | `app/routers/security.py` + frontend `SecurityDashboardPage.jsx` |
