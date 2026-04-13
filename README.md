# Apriori Engine - Production Baseline

Sistem analisis pola peminjaman perpustakaan berbasis association rules (Apriori) dengan:
- Backend API: FastAPI + SQLAlchemy + PostgreSQL
- Frontend: React (Vite) + TypeScript + Tailwind
- Engine: Apriori Python
- Deployment: Docker Compose

## Struktur

- `backend/`: API production.
- `frontend/`: aplikasi web.
- `docs/`: requirement + panduan sidang/client.
- `notebooks/`: eksperimen akademik.
- `data/`: dataset contoh.
- `outputs/`: hasil eksperimen/rules JSON.
- `apriori.py`, `apriori_experiment.py`, `apriori_user_view.py`: script engine standalone.

## Quick Start (Docker)

```bat
docker compose up --build -d
```

Service:
- Frontend: `http://localhost`
- Backend: `http://localhost:8000`
- API docs: `http://localhost:8000/docs`

Seed demo data:
```bat
docker compose exec backend python -m scripts.seed_demo
```

Jalankan analisis:
```bat
curl -X POST "http://localhost:8000/api/analysis/run" ^
  -H "Content-Type: application/json" ^
  -d "{\"run_name\":\"demo-run\",\"min_support\":0.3,\"min_confidence\":0.6,\"min_lift\":1.0}"
```

## Run Lokal Tanpa Docker

Backend:
```bat
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload --port 8000
```

Frontend:
```bat
cd frontend
npm install
copy .env.example .env
npm run dev
```

## Eksperimen Notebook

- `notebooks/Apriori_Experiment.ipynb`
- `notebooks/Demo_Sidang_Apriori.ipynb`
