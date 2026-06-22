# Panduan Client dan Sidang

Dokumen ini membantu client/operator dan mahasiswa menjelaskan sistem saat demo atau sidang.

## 1. Narasi Singkat Sistem

Sistem ini membaca data peminjaman perpustakaan, mengubahnya menjadi transaksi, lalu mencari pola hubungan antara fakultas mahasiswa dan buku yang dipinjam menggunakan algoritma Apriori.

Hasil akhirnya berupa aturan seperti:

`Jika mahasiswa berasal dari Fakultas A, maka cenderung meminjam Buku B.`

Aturan ini dapat dipakai sebagai bahan evaluasi koleksi, rekomendasi pengadaan buku, dan analisis kebutuhan literatur tiap fakultas.

## 2. Alur Demo 5-7 Menit

1. Buka aplikasi web.
2. Tunjukkan panel import CSV.
3. Jelaskan bahwa sistem melakukan preprocessing data.
4. Jalankan analisis Apriori dengan parameter tertentu.
5. Tampilkan tabel hasil rule.
6. Buka detail rule dan jelaskan support, confidence, lift.
7. Tunjukkan riwayat run dan compare run.
8. Tampilkan halaman dokumentasi/diagram jika ditanya perancangan sistem.

## 3. Penjelasan Metrik untuk Sidang

### Support

Support menunjukkan seberapa sering kombinasi `Jika` dan `Maka` muncul pada seluruh transaksi.

Contoh: support 2% berarti 2 dari 100 transaksi mengandung kombinasi tersebut.

### Confidence

Confidence menunjukkan seberapa sering bagian `Maka` benar ketika bagian `Jika` terjadi.

Contoh: confidence 40% berarti dari semua transaksi yang memenuhi `Jika`, sebanyak 40% juga memenuhi `Maka`.

### Lift

Lift menunjukkan apakah hubungan tersebut lebih kuat daripada kejadian acak.

- `lift > 1`: hubungan lebih kuat dari kebetulan
- `lift = 1`: hubungan netral
- `lift < 1`: hubungan lemah

## 4. Jawaban Singkat Jika Ditanya Dosen

### Kenapa memakai Apriori?

Karena Apriori cocok untuk mencari association rules pada data transaksi, dan hasilnya mudah dijelaskan dalam bentuk `Jika -> Maka`.

### Kenapa memakai web jika eksperimen bisa di notebook?

Notebook digunakan untuk validasi metode dan dokumentasi eksperimen. Web digunakan agar client/operator dapat mengimport data, menjalankan analisis, dan membaca hasil tanpa membuka kode Python.

### Kenapa hasil bisa kosong?

Biasanya karena threshold support atau confidence terlalu tinggi, sehingga tidak ada pola yang memenuhi batas minimal.

### Kenapa lift penting?

Confidence saja bisa menipu jika buku tertentu memang sering dipinjam oleh semua fakultas. Lift membantu melihat apakah hubungan fakultas dan buku benar-benar lebih kuat dari baseline.

### Kenapa ada riwayat run?

Agar hasil analisis dapat dibandingkan antar parameter atau antar periode data.

## 5. Checklist Sebelum Presentasi

- Pastikan API aktif: https://api.anisaaaaa.sbs/api/health
- Pastikan web aktif: https://anisaaaaa.sbs
- Siapkan dataset CSV yang valid.
- Jika ingin demo dari nol, klik `Kosongkan Dataset` terlebih dahulu.
- Import dataset.
- Jalankan minimal satu analisis.
- Siapkan contoh satu rule yang akan dijelaskan.
- Buka halaman `/dokumentasi/diagram_skripsi` jika perlu menunjukkan ERD/diagram.

## 6. Contoh Penjelasan Rule

Rule:

`Jika Fakultas:Teknik Informatika maka Buku:Data Mining`

Penjelasan:

Berdasarkan data peminjaman, mahasiswa Teknik Informatika memiliki kecenderungan meminjam buku Data Mining. Nilai support menunjukkan seberapa sering pola ini muncul pada seluruh transaksi. Nilai confidence menunjukkan peluang buku tersebut dipinjam ketika transaksinya berasal dari fakultas tersebut. Nilai lift menunjukkan apakah hubungan itu lebih kuat dibanding peminjaman acak.

## 7. Catatan untuk Client

- Client tidak perlu menjalankan Jupyter Notebook untuk memakai sistem web.
- Client cukup mengakses web, upload CSV, dan membaca hasil.
- Jika dataset berubah total, kosongkan dataset terlebih dahulu agar analisis tidak tercampur.
- Jika hanya ingin menambahkan data baru, import CSV tanpa mengosongkan dataset.
