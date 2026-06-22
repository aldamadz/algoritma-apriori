# Dokumentasi Penggunaan Sistem Apriori Engine

Dokumen ini menjelaskan cara memakai sistem yang sudah berjalan pada production.

## 1. Akses Sistem

- Aplikasi web: https://anisaaaaa.sbs
- Dokumentasi web: https://anisaaaaa.sbs/dokumentasi
- API docs: https://api.anisaaaaa.sbs/docs
- Health check API: https://api.anisaaaaa.sbs/api/health

Jika menjalankan lokal dengan Docker, alamat defaultnya:

- Frontend: http://localhost
- Backend/API docs: http://localhost:8000/docs

## 2. Alur Kerja Utama

1. Buka aplikasi web.
2. Jika ingin memakai dataset baru, klik `Kosongkan Dataset` terlebih dahulu.
3. Upload file CSV pada panel `Import Dataset CSV`.
4. Tunggu proses preprocessing dan penyimpanan data selesai.
5. Isi parameter analisis pada panel `Jalankan Analisis`.
6. Klik tombol untuk menjalankan Apriori.
7. Pilih run pada `Riwayat Analisis`.
8. Baca hasil pada tabel `Hasil Analisis Peminjaman`.
9. Klik `Detail` pada rule yang ingin dijelaskan.

## 3. Fungsi Import CSV

Import CSV digunakan untuk memasukkan data peminjaman ke database. Jadi import bukan hanya membaca file sementara, tetapi menambah data master dan transaksi ke sistem.

Saat import, sistem melakukan:

- validasi file CSV
- deteksi format kolom
- normalisasi data fakultas, mahasiswa, buku, dan tanggal
- pengelompokan baris menjadi transaksi peminjaman
- penyimpanan data fakultas, mahasiswa, buku, transaksi, dan item buku
- pengecekan transaksi duplikat berdasarkan mahasiswa, tanggal, tanggal kembali, dan daftar buku

Jika file yang sama diupload lagi, transaksi yang sama akan dilewati agar tidak menggandakan data.

## 4. Format CSV yang Didukung

### 4.1 Format Standar Sistem

Kolom wajib:

- `transaction_id`
- `student_number`
- `department_code`
- `loan_date` dengan format `YYYY-MM-DD`
- `book_isbn`

Kolom opsional:

- `student_name`
- `department_name`
- `return_date`
- `book_title`
- `book_author`
- `book_category`

Contoh:

```csv
transaction_id,student_number,student_name,department_code,department_name,loan_date,return_date,book_isbn,book_title
TRX001,2024001,Ani,TI,Teknik Informatika,2025-01-10,,BK001,Data Mining
TRX001,2024001,Ani,TI,Teknik Informatika,2025-01-10,,BK002,Algoritma
```

### 4.2 Format Data Perpustakaan Riil

Sistem juga mendukung dataset perpustakaan dengan kolom:

- `no_mhs`
- `nama`
- `fakultas`
- `kd_buku`
- `judul`
- `tgl_pinjam`

Kolom tambahan yang akan ikut dimanfaatkan bila tersedia:

- `tgl_kembali`
- `no_barcode`
- `label1`
- `label2`

Catatan:

- `fakultas` akan dipakai sebagai nama fakultas.
- `kd_buku` dipakai sebagai kode buku. Jika kosong, sistem mencoba memakai `no_barcode`.
- `judul` dipakai sebagai nama buku.
- Tanggal harus dapat dibaca sebagai `YYYY-MM-DD`.

## 5. Kosongkan Dataset

Tombol `Kosongkan Dataset` digunakan saat operator ingin mengganti dataset sepenuhnya.

Data yang dihapus:

- fakultas
- mahasiswa
- buku
- transaksi peminjaman
- item transaksi
- riwayat analisis
- association rules

Gunakan tombol ini sebelum import dataset baru agar hasil analisis tidak tercampur dengan dataset lama.

## 6. Menjalankan Analisis

Panel `Jalankan Analisis` mengirim data ke backend untuk diproses dengan algoritma Apriori.

Parameter utama:

- `Min Support`: batas minimal kemunculan pola pada seluruh transaksi.
- `Min Confidence`: batas minimal kepercayaan aturan.
- `Min Lift`: batas minimal kekuatan asosiasi.

Rekomendasi awal untuk data riil yang besar:

- `min_support`: 0.005 sampai 0.02
- `min_confidence`: 0.02 sampai 0.10
- `min_lift`: 1.00 sampai 1.20

Jika rule kosong, turunkan `min_support` atau `min_confidence`.

## 7. Membaca Hasil Rule

Tabel hasil berisi:

- `Jika`: kondisi awal, biasanya fakultas atau buku.
- `Maka`: rekomendasi atau item yang sering muncul bersama.
- `Support`: persentase seluruh transaksi yang memuat kombinasi tersebut.
- `Confidence`: peluang `Maka` terjadi ketika `Jika` terjadi.
- `Lift`: kekuatan hubungan dibanding kejadian acak.
- `Kekuatan`: label interpretasi berdasarkan nilai lift.

Contoh:

Jika `Fakultas:Teknik Informatika` maka `Buku:Data Mining`.

Artinya mahasiswa Teknik Informatika memiliki kecenderungan meminjam buku Data Mining berdasarkan pola transaksi yang ada.

## 8. Riwayat Analisis

Setiap kali analisis dijalankan, sistem menyimpan satu run baru.

Fitur riwayat:

- memilih run aktif
- melihat parameter yang dipakai
- memfilter run berdasarkan bulan pembuatan
- menghapus run yang tidak diperlukan
- membandingkan dua run

Nomor pada tabel riwayat adalah nomor tampilan, bukan ID database. Jika data dihapus, nomor tampilan akan tetap rapi.

## 9. Troubleshooting Penggunaan

### Hasil rule kosong

Kemungkinan penyebab:

- threshold terlalu tinggi
- dataset terlalu menyebar
- data fakultas atau buku terlalu banyak variasi

Solusi:

- turunkan `min_support`
- turunkan `min_confidence`
- pastikan data sudah terimport
- cek filter pada tabel rules

### Import gagal

Cek hal berikut:

- file harus `.csv`
- encoding sebaiknya UTF-8
- nama kolom sesuai format yang didukung
- tanggal memakai format `YYYY-MM-DD`

### Data terlihat dobel

Jika pernah import file berulang sebelum fitur skip duplikat aktif, gunakan `Kosongkan Dataset`, lalu import ulang satu kali.

### Upload file besar gagal

Pada hosting shared, batas upload dapat dipengaruhi konfigurasi server. Jika file terlalu besar, pecah dataset menjadi beberapa file CSV atau minta penyesuaian limit upload ke provider hosting.
