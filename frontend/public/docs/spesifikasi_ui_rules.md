# Spesifikasi UI Hasil Rules

Dokumen ini menjelaskan desain halaman hasil association rules yang digunakan pada sistem.

## 1. Tujuan Halaman

Halaman `Hasil Analisis Peminjaman` dirancang agar user non-teknis dapat membaca hasil Apriori tanpa harus memahami seluruh proses data mining secara mendalam.

Tujuannya:

- menampilkan rule dalam format `Jika -> Maka`
- menampilkan support, confidence, dan lift
- menyediakan filter rule
- menyediakan dialog detail dengan penjelasan natural
- mendukung pagination agar data besar tidak membebani browser

## 2. Komponen UI Utama

### Summary Cards

Menampilkan ringkasan:

- total rule valid
- rule terkuat berdasarkan lift
- fakultas dominan

### Filter Rules

Filter yang tersedia:

- pencarian fakultas/buku
- filter fakultas
- minimum confidence
- minimum lift
- reset filter

Catatan: filter tanggal tidak digunakan pada tabel hasil rules karena periode analisis sudah ditentukan saat run dibuat. Tabel rules fokus menampilkan hasil dari run yang sedang aktif.

### Rules Table

Kolom tabel:

- No
- Jika
- Maka
- Support
- Confidence
- Lift
- Kekuatan
- Aksi

Nomor pada kolom `No` adalah nomor tampilan berdasarkan halaman, bukan ID database.

### Detail Rule

Dialog detail menjelaskan:

- arti support pada rule tersebut
- arti confidence pada rule tersebut
- arti lift pada rule tersebut
- label kekuatan rule

## 3. Interpretasi Kekuatan Rule

Label kekuatan berdasarkan nilai lift:

- `Sangat Kuat`: lift >= 2
- `Kuat`: 1.2 <= lift < 2
- `Cukup`: 1 <= lift < 1.2
- `Lemah`: lift < 1

Lift dipakai karena dapat menunjukkan apakah hubungan lebih kuat dibanding kejadian acak.

## 4. Endpoint yang Dipakai

Rules page memakai endpoint:

```http
GET /api/analysis/runs/{run_id}/rules
```

Query yang didukung:

- `department_id`
- `q`
- `min_confidence`
- `min_lift`
- `page`
- `limit`
- `sort_by`
- `sort_dir`

Contoh:

```http
GET /api/analysis/runs/1/rules?min_confidence=0.05&min_lift=1&page=1&limit=10
```

## 5. Response API

Contoh response:

```json
{
  "data": [
    {
      "id": 1,
      "antecedent": ["Fakultas:Teknik Informatika"],
      "consequent": ["Buku:Data Mining"],
      "support": 0.021,
      "confidence": 0.37,
      "lift": 2.4,
      "supportCount": 42
    }
  ],
  "meta": {
    "page": 1,
    "limit": 10,
    "total": 1,
    "totalPages": 1
  },
  "summary": {
    "totalRules": 1,
    "topLiftRule": null,
    "dominantDepartment": "Teknik Informatika"
  }
}
```

## 6. Responsivitas

Tabel menggunakan horizontal scroll pada layar kecil agar kolom tetap terbaca. Panel dan kartu ringkasan mengikuti layout responsif agar bisa digunakan di desktop maupun mobile.

## 7. Prinsip Tampilan

- Gunakan bahasa sederhana.
- Hindari menampilkan JSON mentah kepada user.
- Angka support dan confidence ditampilkan dalam persen.
- Lift ditampilkan dua angka desimal.
- Detail rule harus menjelaskan makna angka, bukan hanya menampilkan angka.
