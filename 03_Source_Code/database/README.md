# database/ — Compatibility Entrypoint

Direktori ini adalah **compatibility entrypoint** untuk konfigurasi database.

Implementasi lengkap ada di:
```
03_Source_Code/backend/app/core/database.py   ← SQLAlchemy engine, session, Base
03_Source_Code/backend/app/models/            ← Semua model/entitas DB
03_Source_Code/backend/app/core/crypto.py     ← AES-256-GCM untuk enkripsi kolom
```

## Skema Database (Tabel Utama)

```
users
  user_id        VARCHAR PK
  nama           VARCHAR (plaintext)
  email          VARCHAR UNIQUE
  password       VARCHAR (bcrypt hash)
  no_telp        VARCHAR (AES-256-GCM terenkripsi)
  role           ENUM('mahasiswa', 'umkm', 'admin')
  status         ENUM('aktif', 'nonaktif')
  created_at     TIMESTAMP

pesanan
  pesanan_id     VARCHAR PK
  mahasiswa_id   FK → users.user_id
  umkm_id        FK → users.user_id
  total          INTEGER
  status         VARCHAR
  tanda_tangan   TEXT  ← RSA-2048 signature (base64)
  created_at     TIMESTAMP

audit_logs                        ← API request audit log
  id             VARCHAR PK
  user_id        FK → users.user_id (nullable)
  method         VARCHAR(10)
  endpoint       VARCHAR(255)
  status_code    INTEGER
  ip_address     VARCHAR(50)
  user_agent     VARCHAR(255)
  duration_ms    INTEGER
  created_at     TIMESTAMP
```

## Enkripsi Kolom Sensitif

Kolom `no_telp` dienkripsi menggunakan AES-256-GCM sebelum disimpan ke DB.
Enkripsi/dekripsi dilakukan di level service (bukan di level DB) via `app/core/crypto.py`.

```python
from app.core.crypto import encrypt, decrypt

encrypted = encrypt("081234567890")   # → base64 string
original  = decrypt(encrypted)        # → "081234567890"
```
