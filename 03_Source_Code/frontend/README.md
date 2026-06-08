# Frontend — IPB Food Hub & UMKM

Kode React + Vite untuk antarmuka pengguna IPB Food Hub.
File-file yang relevan untuk modul keamanan (sudah tersedia di folder ini):

```
frontend/src/
├── pages/
│   ├── LoginPage.jsx              ← Form login dengan penanganan error auth
│   ├── RegisterPage.jsx           ← Form registrasi
│   └── SecurityDashboardPage.jsx  ← Dashboard audit log (khusus admin)
├── services/
│   └── api.js                     ← Axios instance dengan Bearer token header
└── App.jsx                        ← Route protection (redirect jika tidak login)
```

## Cara Menjalankan

```bash
npm install
npm run dev
```

Pastikan `VITE_API_URL` di file `.env` mengarah ke backend:
```env
VITE_API_URL=http://localhost:8000
```
