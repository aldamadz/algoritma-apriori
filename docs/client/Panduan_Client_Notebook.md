# Panduan Client Menjalankan Notebook

Dokumen ini untuk client agar dapat menjalankan notebook analisis secara lokal.

## 1. Kebutuhan

- Windows + Python 3.10+ terpasang.
- Google Colab atau Python 3.10+ dengan JupyterLab.
- File notebook `.ipynb`.
- Dataset dalam format CSV.

## 2. Cara Menjalankan (Paling Mudah)

### Opsi A: Double click file `.bat`

1. Buka folder `client/`.
2. Jalankan `start_notebook_client.bat`.
3. Tunggu proses install dependency selesai.
4. Browser akan membuka JupyterLab otomatis.

### Opsi B: PowerShell

```powershell
.\client\start_notebook_client.ps1
```

## 3. Notebook yang Dipakai

- `notebooks/Demo_Sidang_Apriori.ipynb`
- `notebooks/Apriori_Experiment.ipynb`

Notebook bersifat mandiri. Client tidak perlu mengunduh repository, memiliki akun GitHub, atau menyiapkan file Python tambahan.

## 4. Upload Dataset

Pada sel **Upload dan Preprocessing Dataset**:

1. Jalankan sel.
2. Di Google Colab, klik **Choose Files** lalu pilih satu CSV.
3. Di Jupyter lokal, masukkan path CSV atau tekan Enter untuk memakai dataset contoh.
4. Periksa ringkasan kolom, jumlah baris, duplikat, jumlah transaksi, dan contoh basket.

Dataset contoh tetap tersedia:

- `dataset.csv` (dataset utama peminjaman UIN)
- `data/dataset_import_1000_transaksi.csv`
- `data/dataset_import_5000_transaksi.csv`

Format yang dikenali otomatis:

| Bentuk | Key transaksi | Item |
|---|---|---|
| Sederhana | `transaction_id` | `item` |
| Import perpustakaan | `transaction_id` | `department_code`, `book_title` |
| Peminjaman UIN | `no_mhs`, `tgl_pinjam` | `fakultas`, `judul` |

Untuk nama kolom lain, isi mapping manual di notebook:

```python
TRANSACTION_KEY_COLS = ["customer", "date"]
ITEM_SPECS = [("product", "Produk")]
```

Satu baris CSV merepresentasikan satu item. Semua baris dengan key transaksi yang sama digabung menjadi satu basket. Nilai kosong dilewati dan item berulang dalam transaksi yang sama hanya dihitung sekali.

## 5. Alur Proses Dataset

```text
Upload/pilih CSV
-> baca dan validasi header
-> tentukan key transaksi dan kolom item
-> kelompokkan baris berdasarkan key transaksi
-> bersihkan nilai kosong dan item duplikat
-> bentuk basket transaksi
-> hitung frequent itemsets
-> bentuk association rules
```

## 6. Jika Gagal karena Permission Jupyter

Script sudah mengatur:
- `JUPYTER_RUNTIME_DIR`
- `JUPYTER_CONFIG_DIR`
- `JUPYTER_DATA_DIR`

ke folder project lokal, jadi error akses `AppData\Roaming\jupyter` harusnya tidak muncul lagi.
