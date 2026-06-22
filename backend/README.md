# Backend API - Apriori Engine

Backend menggunakan FastAPI, SQLAlchemy, dan Psycopg untuk mengelola data peminjaman serta menjalankan analisis Apriori.

## 1. Run Lokal

```bat
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Jika tidak ada `.env`, backend memakai SQLite lokal sebagai default cepat.

Jika ingin memakai PostgreSQL, set `DATABASE_URL`:

```env
DATABASE_URL=postgresql+psycopg://USER:PASSWORD@localhost:5432/apriori_db
```

## 2. Run Production Shared Hosting

Production berjalan pada Python App cPanel/LiteSpeed:

- Python: 3.9.23
- Startup file: `passenger_wsgi.py`
- Entry point: `application`
- API URL: https://api.anisaaaaa.sbs

Environment production:

```env
APP_ENV=production
DEBUG=false
DATABASE_URL=postgresql+psycopg://USER:PASSWORD@/DB_NAME?host=/var/run/postgresql
CORS_ORIGINS=https://anisaaaaa.sbs,https://www.anisaaaaa.sbs
```

Restart:

```bash
cd /home/wurdgtgl/api.anisaaaaa.sbs
find . -name "*.pyc" -delete
find . -type d -name "__pycache__" -exec rm -rf {} +
touch tmp/restart.txt
```

## 3. Endpoint Utama

Health:

- `GET /api/health`

Master:

- `GET/POST /api/departments`
- `GET/POST /api/students`
- `GET/POST /api/books`

Transaksi:

- `GET /api/transactions`
- `POST /api/transactions`
- `GET /api/transactions/summary`
- `POST /api/transactions/import-csv`
- `DELETE /api/transactions/dataset`

Analisis:

- `POST /api/analysis/run`
- `GET /api/analysis/runs`
- `GET /api/analysis/runs/{id}`
- `DELETE /api/analysis/runs/{id}`
- `GET /api/analysis/runs/{id}/rules`

## 4. Format CSV Import

Format standar wajib:

- `transaction_id`
- `student_number`
- `department_code`
- `loan_date` format `YYYY-MM-DD`
- `book_isbn`

Kolom opsional:

- `student_name`
- `department_name`
- `return_date`
- `book_title`
- `book_author`
- `book_category`

Format perpustakaan riil yang didukung:

- `no_mhs`
- `nama`
- `fakultas`
- `kd_buku`
- `judul`
- `tgl_pinjam`

Kolom tambahan yang dimanfaatkan bila ada:

- `tgl_kembali`
- `no_barcode`
- `label1`
- `label2`

## 5. Dokumentasi Otomatis

FastAPI otomatis menyediakan:

- Swagger UI: `/docs`
- ReDoc: `/redoc`
- OpenAPI JSON: `/openapi.json`

Production:

- https://api.anisaaaaa.sbs/docs
