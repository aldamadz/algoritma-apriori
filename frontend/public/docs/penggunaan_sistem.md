# Dokumentasi Penggunaan Sistem Apriori Engine (As-Built)

Dokumen ini menjelaskan penggunaan sistem sesuai implementasi yang aktif saat ini.

## 1. Akses Sistem

- Aplikasi web: `http://localhost`
- API docs: `http://localhost:8000/docs`
- Dokumentasi web: `http://localhost/dokumentasi`

## 2. Menjalankan Sistem

```bat
docker compose up -d --build
docker compose ps
```

Service yang harus `Up`:
- `apriori-frontend`
- `apriori-backend`
- `apriori-postgres` (mode lokal)

Jika mode server menggunakan DB existing:

```bat
docker compose -f docker-compose.server.yml up -d --build
```

## 3. Data CSV Import

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

## 4. Generate Dataset Otomatis

Script:
- [generate_import_dataset.py](D:\Koding\algoritma apriori\data\generate_import_dataset.py)

Contoh:

```bat
python data\generate_import_dataset.py --transactions 1000
python data\generate_import_dataset.py --transactions 5000
```

## 5. Alur Penggunaan UI

1. Import data lewat panel `Import Dataset CSV`.
2. Jalankan analisis lewat panel `Jalankan Analisis`.
3. Pilih run aktif pada panel `Riwayat Analisis`.
4. Lihat hasil rule pada tabel `Hasil Analisis Peminjaman`.
5. Jika perlu, klik `Detail` untuk membaca rule per baris.

## 6. Riwayat dan Operasional Run

Fitur pada panel `Riwayat Analisis`:
- filter run berdasarkan bulan
- pilih run aktif
- hapus run

Fitur panel `Bandingkan 2 Run`:
- bandingkan total rules
- lihat delta rules
- lihat top rule masing-masing run
- lihat jurusan dominan masing-masing run

## 7. Membaca Metrik

- `Support`: frekuensi rule pada seluruh transaksi.
- `Confidence`: tingkat keandalan rule.
- `Lift`: kekuatan asosiasi relatif terhadap baseline.

Interpretasi lift:
- `> 1` bermakna
- `= 1` netral
- `< 1` lemah

## 8. Parameter Awal yang Disarankan

Untuk dataset besar:
- `min_support = 0.05`
- `min_confidence = 0.30`
- `min_lift = 0.80` (saat proses mining)

Filter hasil:
- `min_confidence >= 0.30`
- `min_lift >= 1.00`

## 9. Troubleshooting

### 9.1 Hasil rule kosong

- Turunkan threshold (support/confidence).
- Jalankan run baru.
- Reset filter di tabel rules.

### 9.2 Import gagal

- Cek format kolom wajib.
- Cek encoding UTF-8.
- Cek format tanggal `YYYY-MM-DD`.

### 9.3 Upload besar kena 413

- Sudah disiapkan limit Nginx `client_max_body_size 50M`.
- Rebuild frontend jika belum aktif:

```bat
docker compose up -d --build frontend
```

## 10. Endpoint Operasional

- `POST /api/transactions/import-csv`
- `POST /api/analysis/run`
- `GET /api/analysis/runs`
- `DELETE /api/analysis/runs/{id}`
- `GET /api/analysis/runs/{id}/rules`
