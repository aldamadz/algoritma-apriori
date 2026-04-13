# Spesifikasi UI Rules (React + Shadcn)

Dokumen ini adalah blueprint implementasi halaman hasil aturan asosiasi agar mudah dipahami user non-teknis.

## 1. Tujuan Halaman

- Menampilkan aturan asosiasi dalam bahasa sederhana (`Jika` -> `Maka`).
- Memudahkan filter, pencarian, sorting, dan interpretasi rule.
- Menyediakan detail rule untuk kebutuhan presentasi dan keputusan operasional.

## 2. Struktur Layout Halaman

1. `PageHeader`
- Judul: `Hasil Analisis Peminjaman`
- Subjudul: periode + parameter analisis

2. `SummaryCards` (3 kartu)
- `Total Rule Valid`
- `Rule Terkuat (Lift Tertinggi)`
- `Jurusan Paling Dominan`

3. `FilterBar`
- Select `Jurusan`
- Date range `Periode`
- Input/slider `Min Confidence`
- Input/slider `Min Lift`
- Search `kata kunci buku/jurusan`
- Tombol `Reset Filter`

4. `RulesTable`
- Tabel utama hasil aturan
- Sorting + pagination
- Aksi detail

5. `RuleDetailDialog`
- Modal detail rule dalam bahasa natural
- Metrik + interpretasi singkat

## 3. Komponen React (Disarankan)

- `src/features/rules/components/rules-page.tsx`
- `src/features/rules/components/rules-summary-cards.tsx`
- `src/features/rules/components/rules-filter-bar.tsx`
- `src/features/rules/components/rules-table.tsx`
- `src/features/rules/components/rule-strength-badge.tsx`
- `src/features/rules/components/rule-detail-dialog.tsx`
- `src/features/rules/hooks/use-rules-query.ts`
- `src/features/rules/types.ts`

## 4. TypeScript Types

```ts
export type AssociationRule = {
  id: string;
  antecedent: string[];
  consequent: string[];
  support: number;      // 0..1
  confidence: number;   // 0..1
  lift: number;         // >= 0
  supportCount: number;
};

export type RulesQueryParams = {
  analysisRunId: string;
  departmentId?: string;
  q?: string;
  minConfidence?: number;
  minLift?: number;
  page?: number;
  limit?: number;
  sortBy?: "lift" | "confidence" | "support";
  sortDir?: "asc" | "desc";
  periodStart?: string; // YYYY-MM-DD
  periodEnd?: string;   // YYYY-MM-DD
};

export type RulesApiResponse = {
  data: AssociationRule[];
  meta: {
    page: number;
    limit: number;
    total: number;
    totalPages: number;
  };
  summary: {
    totalRules: number;
    topLiftRule?: AssociationRule;
    dominantDepartment?: string;
  };
};
```

## 5. Kolom Tabel (UX Non-Teknis)

1. `No`
2. `Jika` (antecedent)
3. `Maka` (consequent)
4. `Support` (format `%`)
5. `Confidence` (format `%`)
6. `Lift` (2 desimal)
7. `Kekuatan Rule` (badge)
8. `Aksi` (`Detail`)

### Mapping Badge Kekuatan

- `Sangat Kuat`: `lift >= 2`
- `Kuat`: `1.2 <= lift < 2`
- `Cukup`: `1 <= lift < 1.2`
- `Lemah`: `lift < 1`

## 6. Kontrak API (Backend)

### Endpoint

- `GET /api/analysis/runs/:id/rules`

### Query

- `department_id`
- `q`
- `min_confidence`
- `min_lift`
- `page`
- `limit`
- `sort_by` (`lift|confidence|support`)
- `sort_dir` (`asc|desc`)
- `period_start`
- `period_end`

### Response contoh

```json
{
  "data": [
    {
      "id": "rule_001",
      "antecedent": ["Jurusan TI"],
      "consequent": ["Buku AI Dasar"],
      "support": 0.3333,
      "confidence": 0.875,
      "lift": 1.92,
      "supportCount": 42
    }
  ],
  "meta": {
    "page": 1,
    "limit": 10,
    "total": 125,
    "totalPages": 13
  },
  "summary": {
    "totalRules": 125,
    "topLiftRule": {
      "id": "rule_088",
      "antecedent": ["Jurusan SI"],
      "consequent": ["Buku Data Mining"],
      "support": 0.21,
      "confidence": 0.90,
      "lift": 2.35,
      "supportCount": 25
    },
    "dominantDepartment": "Teknik Informatika"
  }
}
```

## 7. Formatting Helper (Frontend)

```ts
export const toPercent = (value: number) => `${(value * 100).toFixed(2)}%`;
export const toLift = (value: number) => value.toFixed(2);
```

## 8. State Management

- Gunakan `TanStack Query` untuk fetch data rules.
- Gunakan `URLSearchParams` untuk sinkronisasi filter ke URL.
- Debounce search (`300ms`) supaya query efisien.

## 9. Komponen Shadcn yang Dipakai

- `Card` untuk summary
- `Data Table` (`Table`) untuk list rules
- `Select` untuk jurusan dan sort
- `Input` untuk search
- `Slider` atau `Input Number` untuk min confidence/lift
- `Dialog` untuk detail rule
- `Badge` untuk kekuatan rule
- `Pagination` untuk navigasi halaman

## 10. Isi Rule Detail Dialog

- Judul: `Detail Aturan`
- Kalimat natural:
- `Mahasiswa [Jurusan TI] cenderung meminjam [Buku AI Dasar].`
- Nilai:
- Support: `33.33%`
- Confidence: `87.50%`
- Lift: `1.92`
- Interpretasi singkat:
- `Hubungan ini tergolong kuat dan layak dipertimbangkan untuk rekomendasi pengadaan.`

## 11. Kriteria Selesai UI

- User bisa melihat top rules tanpa paham istilah data mining teknis.
- User bisa filter aturan berdasarkan jurusan/periode/kekuatan.
- User bisa membuka detail rule dan memahami maknanya.
- Tabel responsif untuk desktop dan mobile.
