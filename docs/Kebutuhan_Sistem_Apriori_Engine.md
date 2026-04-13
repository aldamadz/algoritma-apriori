# Sistem Analisis Pola Peminjaman Perpustakaan (Apriori Engine)

Dokumen ini adalah versi **as-built** (sesuai implementasi yang sudah terpasang saat ini), bukan rencana awal.

## 1. Tujuan Sistem

- Menambang aturan asosiasi antara item `Jurusan:*` dan `Buku:*` dari transaksi peminjaman.
- Menyediakan antarmuka web untuk import data, menjalankan analisis, melihat hasil, dan membandingkan run.

## 2. Teknologi yang Terpasang

- Frontend: `React + Vite + TypeScript + Tailwind`
- UI Components: komponen internal kompatibel pola `shadcn` (`card`, `button`, `table`, `dialog`, dll)
- Backend API: `FastAPI + SQLAlchemy`
- Data Mining Engine: Python Apriori (custom implementation)
- Database:
  - Local/dev cepat: `SQLite` (default di config)
  - Container/production baseline: `PostgreSQL`
- Container: `Docker + Docker Compose`
- Reverse proxy frontend: `Nginx` (dengan proxy `/api`)

## 3. Fitur yang Sudah Ada

- Import transaksi via CSV dari frontend.
- Jalankan analisis Apriori dari frontend.
- Riwayat run analisis:
  - pilih run aktif
  - filter bulan
  - hapus run
  - bandingkan 2 run
- Tabel aturan asosiasi:
  - support, confidence, lift
  - filter, pagination, detail rule
- Halaman dokumentasi web:
  - `/dokumentasi`
  - `/dokumentasi/penggunaan_sistem`
  - `/dokumentasi/kebutuhan_sistem`
  - dst.

## 4. Fitur yang Belum Diimplementasikan

- Auth/login multi-user.
- Role-based access control.
- Ekspor PDF/Excel.
- Scheduler analisis otomatis.
- Observability production penuh (metrics tracing dashboard).

## 5. Desain Data (Aktif)

Tabel utama:
- `departments`
- `students`
- `books`
- `loan_transactions`
- `loan_transaction_items`
- `analysis_runs`
- `association_rules`

Catatan:
- Tabel `users` dan `frequent_itemsets` belum dipakai di implementasi saat ini.

## 6. Endpoint API (Aktif)

Health:
- `GET /api/health`

Master:
- `GET/POST /api/departments`
- `GET/POST /api/students`
- `GET/POST /api/books`

Transaksi:
- `GET /api/transactions`
- `POST /api/transactions`
- `POST /api/transactions/import-csv`

Analisis:
- `POST /api/analysis/run`
- `GET /api/analysis/runs`
- `GET /api/analysis/runs/{id}`
- `DELETE /api/analysis/runs/{id}`
- `GET /api/analysis/runs/{id}/rules`

## 7. Format CSV Import (Aktif)

Kolom wajib:
- `transaction_id`
- `student_number`
- `department_code`
- `loan_date` (`YYYY-MM-DD`)
- `book_isbn`

Kolom opsional:
- `student_name`
- `department_name`
- `book_title`
- `book_author`
- `book_category`

## 8. Alur Analisis di Sistem

1. User import CSV.
2. Sistem menyimpan master dan transaksi.
3. User menjalankan `POST /api/analysis/run` (via panel frontend).
4. Backend membentuk basket per transaksi:
- `Jurusan:{nama_jurusan}`
- `Buku:{judul_buku}`
5. Engine Apriori menghitung rules.
6. Rule disimpan ke `association_rules`.
7. Frontend menampilkan hasil berdasarkan `run_id`.

## 9. Rekomendasi Parameter Operasional

Untuk dataset besar acak (mis. 1000+ transaksi):
- `min_support = 0.05`
- `min_confidence = 0.30`
- `min_lift = 0.8` saat mining

Untuk filter tampilan hasil:
- `min_confidence >= 0.30`
- `min_lift >= 1.0`

## 10. Deployment yang Digunakan

Service Docker Compose:
- `frontend` (Nginx + static Vite build)
- `backend` (FastAPI)
- `postgres` (PostgreSQL)

Command:

```bat
docker compose up -d --build
```

## 11. Batasan Sistem Saat Ini

- ID run tidak akan mengisi nomor yang terhapus (normal behavior sequence DB).
- Kualitas rules sangat bergantung pada kualitas data dan threshold.
- Dataset besar perlu tuning parameter agar rules tidak kosong atau terlalu banyak.

## 12. Status

Dokumen ini sinkron dengan implementasi yang aktif per update terakhir April 2026.
