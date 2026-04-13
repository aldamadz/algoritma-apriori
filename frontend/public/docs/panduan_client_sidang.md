# Panduan Client dan Sidang

## A. Narasi Ringkas ke Client

Narasi yang direkomendasikan:

"Sistem membaca data peminjaman, membentuk pola, lalu menghasilkan aturan hubungan antara jurusan dan buku.  
Hasil aturan dipakai sebagai dasar rekomendasi pengadaan dan evaluasi koleksi."

## B. Makna Metrik (Versi Singkat)

- `Support`: seberapa sering pola muncul di seluruh transaksi.
- `Confidence`: seberapa sering konsekuen benar saat anteseden terjadi.
- `Lift`: seberapa bermakna hubungan dibanding kebetulan.
- Rule operasional umumnya diprioritaskan jika `lift > 1`.

## C. Alur Demo Sidang (5-7 menit)

1. Tampilkan tujuan sistem.
2. Tampilkan format data dan proses import.
3. Tunjukkan run analisis dan hasil rules.
4. Tunjukkan riwayat run + perbandingan 2 run.
5. Berikan kesimpulan rekomendasi koleksi.

## D. Skrip Jawaban Cepat saat Ditanya Dosen

### "Kenapa pakai Apriori?"
- Karena sesuai untuk association rules dan mudah diinterpretasi untuk data transaksi.

### "Kenapa ada threshold support/confidence?"
- Untuk mengendalikan kualitas aturan dan mengurangi noise.

### "Kenapa butuh lift?"
- Karena confidence saja belum cukup; lift mengukur kekuatan terhadap baseline.

### "Kenapa ada notebook dan web?"
- Notebook untuk validasi eksperimen.
- Web untuk operasional harian user perpustakaan.

### "Kenapa run lama tidak hilang meski ada run baru?"
- Karena tiap run disimpan sebagai riwayat analisis untuk audit dan perbandingan periodik.

## E. Checklist Sebelum Presentasi

- Data demo siap (1000/5000 transaksi atau data riil).
- Sistem web berjalan (`frontend/backend/postgres` up).
- Minimal 2 run tersedia untuk demo compare.
- Top rules sudah dipahami interpretasinya.
- Notebook dapat dibuka jika diperlukan lampiran eksperimen.

## F. Command Cadangan (Jika Notebook Bermasalah)

```bat
python apriori_user_view.py --csv data/sample_transactions.csv --min-support 0.05 --min-confidence 0.3 --min-lift 0.8 --top-n 10 --json-out outputs/rules_backend.json
```

```bat
python apriori_experiment.py --csv data/sample_transactions.csv --supports 0.2,0.3,0.4 --confidences 0.5,0.6,0.7 --out-dir outputs/experiment_output
```
