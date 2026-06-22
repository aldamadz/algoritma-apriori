# Apriori Engine - Sistem Analisis Pola Peminjaman Perpustakaan

Apriori Engine adalah sistem berbasis web untuk menemukan association rules antara fakultas mahasiswa dan koleksi buku yang dipinjam.

Production aktif:

- Frontend: https://anisaaaaa.sbs
- Backend API: https://api.anisaaaaa.sbs
- API Docs: https://api.anisaaaaa.sbs/docs
- Dokumentasi web: https://anisaaaaa.sbs/dokumentasi

## 1. Stack Teknologi

Frontend:

- React
- Vite
- TypeScript
- Tailwind CSS
- komponen UI internal bergaya shadcn
- Ant Design DatePicker
- TanStack Query
- React Helmet Async

Backend:

- FastAPI
- SQLAlchemy
- Psycopg 3
- Pydantic Settings
- Python 3.9+

Database:

- PostgreSQL untuk production
- SQLite sebagai default lokal cepat jika `DATABASE_URL` tidak dioverride

Eksperimen:

- Jupyter Notebook
- Script Python Apriori standalone

## 2. Struktur Project

```text
backend/                  FastAPI API
frontend/                 React/Vite frontend
frontend/public/docs/     Dokumentasi yang tampil di /dokumentasi
notebooks/                Notebook eksperimen dan demo sidang
data/                     Dataset contoh/generator
outputs/                  Output eksperimen
scripts/                  Script pendukung
```

## 3. Alur Penggunaan Sistem

1. User membuka web.
2. User mengimport CSV.
3. Sistem melakukan preprocessing dan menyimpan data ke database.
4. User menjalankan analisis Apriori.
5. Backend menyimpan hasil run dan association rules.
6. User membaca rules pada tabel hasil analisis.
7. User dapat membandingkan run atau menghapus run.

## 4. Format CSV

Format standar:

```csv
transaction_id,student_number,student_name,department_code,department_name,loan_date,return_date,book_isbn,book_title
TRX001,2024001,Ani,TI,Teknik Informatika,2025-01-10,,BK001,Data Mining
```

Format data perpustakaan riil juga didukung dengan kolom:

- `no_mhs`
- `nama`
- `fakultas`
- `kd_buku`
- `judul`
- `tgl_pinjam`

## 5. Run Lokal dengan Docker

```bat
docker compose up -d --build
```

Akses lokal:

- Frontend: http://localhost
- Backend: http://localhost:8000
- API docs: http://localhost:8000/docs

## 6. Run Lokal Tanpa Docker

Backend:

```bat
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Frontend:

```bat
cd frontend
npm install
copy .env.example .env
npm run dev
```

Isi `.env` frontend lokal:

```env
VITE_API_BASE_URL=http://localhost:8000
```

## 7. Build Frontend Production

```powershell
cd frontend
$env:VITE_API_BASE_URL='https://api.anisaaaaa.sbs'
npm run build
```

Upload isi `frontend/dist` ke folder domain frontend hosting.

## 8. Deploy Backend Shared Hosting

Folder backend hosting:

```text
/home/wurdgtgl/api.anisaaaaa.sbs
```

File penting:

- `app/`
- `requirements.txt`
- `passenger_wsgi.py`
- `.htaccess`
- `tmp/restart.txt`

Restart backend:

```bash
cd /home/wurdgtgl/api.anisaaaaa.sbs
find . -name "*.pyc" -delete
find . -type d -name "__pycache__" -exec rm -rf {} +
touch tmp/restart.txt
```

## 9. Dokumentasi Web

Dokumen yang tampil di aplikasi berada di:

```text
frontend/public/docs
```

Daftar halaman:

- `/dokumentasi/penggunaan_sistem`
- `/dokumentasi/kebutuhan_sistem`
- `/dokumentasi/deployment_production`
- `/dokumentasi/api_backend`
- `/dokumentasi/panduan_client_sidang`
- `/dokumentasi/spesifikasi_ui_rules`
- `/dokumentasi/diagram_skripsi`

## 10. Notebook

Notebook digunakan untuk eksperimen akademik dan validasi metode, sedangkan web digunakan untuk operasional client.

Contoh:

- `notebooks/Apriori_Experiment.ipynb`
- `notebooks/Demo_Sidang_Apriori.ipynb`

## 11. Verifikasi Production

```text
https://anisaaaaa.sbs
https://anisaaaaa.sbs/dokumentasi
https://api.anisaaaaa.sbs/api/health
https://api.anisaaaaa.sbs/docs
```
