# Frontend Skeleton Rules Page

Folder ini berisi skeleton komponen React + shadcn untuk halaman hasil aturan asosiasi.

## Lokasi

- `frontend/src/features/rules`

## Cara Pakai Cepat

1. Pastikan project Vite React TS sudah punya:
- `@tanstack/react-query`
- komponen shadcn (`button`, `card`, `dialog`, `input`, `select`, `table`, `badge`)

2. Set env:

```env
VITE_API_BASE_URL=http://localhost:3000
```

3. Render halaman:

```tsx
import { RulesPage } from "@/features/rules";

export default function RulesRoute() {
  return (
    <RulesPage
      analysisRunId="run_2026_04_13"
      departments={[
        { label: "Teknik Informatika", value: "dept_ti" },
        { label: "Sistem Informasi", value: "dept_si" },
      ]}
    />
  );
}
```

## Catatan

- Komponen ini asumsi backend tersedia di:
- `GET /api/analysis/runs/:id/rules`
- Pastikan alias path `@/` sudah dikonfigurasi di Vite/TSConfig.
