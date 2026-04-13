# Panduan Client Menjalankan Notebook

Dokumen ini untuk client agar dapat menjalankan notebook analisis secara lokal.

## 1. Kebutuhan

- Windows + Python 3.10+ terpasang.
- Folder project lengkap (termasuk `notebooks/` dan `data/`).

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

## 4. Dataset

- Contoh:
- `data/dataset_import_1000_transaksi.csv`
- `data/dataset_import_5000_transaksi.csv`

Untuk generate dataset baru:

```bat
python data\generate_import_dataset.py --transactions 5000
```

## 5. Jika Gagal karena Permission Jupyter

Script sudah mengatur:
- `JUPYTER_RUNTIME_DIR`
- `JUPYTER_CONFIG_DIR`
- `JUPYTER_DATA_DIR`

ke folder project lokal, jadi error akses `AppData\Roaming\jupyter` harusnya tidak muncul lagi.
