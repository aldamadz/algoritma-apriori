# Kebutuhan Sistem Apriori Engine

Dokumen ini menjelaskan kebutuhan sistem sesuai implementasi yang sedang digunakan.

## 1. Tujuan Sistem

Sistem dibuat untuk menemukan pola asosiasi antara fakultas mahasiswa dan koleksi buku yang dipinjam. Hasilnya digunakan untuk membantu evaluasi koleksi, rekomendasi pengadaan, dan bahan analisis skripsi berbasis data mining.

## 2. Stack Production yang Terpasang

### Frontend

- React
- Vite
- TypeScript
- Tailwind CSS
- Komponen UI internal bergaya shadcn
- Ant Design DatePicker
- TanStack Query
- React Helmet Async

Alamat production:

- https://anisaaaaa.sbs

### Backend

- FastAPI
- SQLAlchemy
- Psycopg 3
- Pydantic Settings
- Python 3.9.23 pada hosting
- Passenger WSGI pada cPanel/LiteSpeed
- Adapter WSGI custom untuk menjalankan FastAPI pada shared hosting

Alamat production:

- https://api.anisaaaaa.sbs

### Database

- PostgreSQL hosting
- Database: `wurdgtgl_apriori_db`
- Tabel dibuat otomatis saat aplikasi backend startup

### Eksperimen Akademik

- Jupyter Notebook untuk validasi metode, eksplorasi dataset, grafik, dan bahan laporan skripsi
- Script Python Apriori standalone untuk eksperimen non-web

## 3. Kebutuhan Browser User

User cukup memakai browser modern:

- Google Chrome
- Microsoft Edge
- Mozilla Firefox

Tidak perlu install Python, Node.js, atau PostgreSQL untuk memakai sistem production.

## 4. Kebutuhan Operator/Admin

Operator perlu memahami:

- format CSV yang didukung
- cara mengosongkan dataset sebelum import dataset baru
- cara memilih parameter support, confidence, dan lift
- cara membaca rule hasil Apriori
- cara menggunakan riwayat run dan compare run

## 5. Kebutuhan Server Production

Server production yang dipakai saat ini:

- hosting dengan dukungan Python App
- PostgreSQL
- domain/subdomain
- SSL aktif
- akses File Manager atau SSH

Konfigurasi domain:

- Frontend statis: `anisaaaaa.sbs`
- Backend API: `api.anisaaaaa.sbs`

Environment backend yang dibutuhkan:

```env
APP_ENV=production
DEBUG=false
DATABASE_URL=postgresql+psycopg://USER:PASSWORD@/DB_NAME?host=/var/run/postgresql
CORS_ORIGINS=https://anisaaaaa.sbs,https://www.anisaaaaa.sbs
```

## 6. Struktur Data Utama

Tabel aktif:

- `departments`: data fakultas
- `students`: data mahasiswa
- `books`: data buku
- `loan_transactions`: data transaksi peminjaman
- `loan_transaction_items`: daftar buku pada setiap transaksi
- `analysis_runs`: riwayat eksekusi analisis
- `association_rules`: hasil aturan asosiasi

## 7. Fitur Sistem

Fitur yang sudah tersedia:

- import CSV dari frontend
- kosongkan dataset
- daftar mahasiswa dengan pagination
- daftar buku dengan pagination
- daftar transaksi dengan pagination
- grafik ringkasan transaksi per bulan
- menjalankan analisis Apriori
- riwayat analisis
- hapus run analisis
- compare dua run
- tabel rules dengan filter dan pagination
- detail rule dengan penjelasan support, confidence, dan lift
- dokumentasi web pada `/dokumentasi`

## 8. Batasan Sistem

- Belum ada login multi-user.
- Belum ada role-based access control.
- Belum ada ekspor PDF/Excel dari UI.
- Kualitas rule sangat bergantung pada kualitas dataset dan threshold.
- Shared hosting memiliki batas resource, sehingga dataset sangat besar perlu diuji bertahap.

## 9. Kebutuhan Lokal Developer

Jika project dijalankan lokal:

- Node.js untuk frontend
- Python 3.9+ untuk backend
- Docker Desktop jika memakai Docker Compose
- PostgreSQL jika tidak memakai SQLite atau container

Mode paling mudah untuk developer:

```bat
docker compose up -d --build
```

Mode frontend lokal:

```bat
cd frontend
npm install
copy .env.example .env
npm run dev
```

Mode backend lokal:

```bat
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```
