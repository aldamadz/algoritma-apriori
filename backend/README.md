# Backend API (FastAPI)

## Run Lokal

```bat
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload --port 8000
```

Catatan:
- Default `.env.example` memakai SQLite untuk local cepat.
- Jika ingin PostgreSQL, ganti `DATABASE_URL` di `.env`.

## Seed Data Demo

```bat
cd backend
python -m scripts.seed_demo
```

## Endpoint Utama

- `GET /api/health`
- `GET/POST /api/departments`
- `GET/POST /api/students`
- `GET/POST /api/books`
- `GET/POST /api/transactions`
- `POST /api/transactions/import-csv`
- `POST /api/analysis/run`
- `GET /api/analysis/runs`
- `GET /api/analysis/runs/{id}`
- `GET /api/analysis/runs/{id}/rules`

## Format CSV Import

Kolom wajib:
- `transaction_id`
- `student_number`
- `department_code`
- `loan_date` (format `YYYY-MM-DD`)
- `book_isbn`

Kolom opsional:
- `student_name`
- `department_name`
- `book_title`
- `book_author`
- `book_category`
