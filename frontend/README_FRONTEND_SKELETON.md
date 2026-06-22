# Frontend Apriori Engine

Frontend adalah aplikasi React/Vite untuk mengoperasikan sistem Apriori Engine.

## 1. Stack

- React
- Vite
- TypeScript
- Tailwind CSS
- TanStack Query
- Ant Design DatePicker
- React Helmet Async

## 2. Run Lokal

```bat
cd frontend
npm install
copy .env.example .env
npm run dev
```

Isi `.env` lokal:

```env
VITE_API_BASE_URL=http://localhost:8000
```

## 3. Build Production

```powershell
cd frontend
$env:VITE_API_BASE_URL='https://api.anisaaaaa.sbs'
npm run build
```

Hasil build berada di:

```text
frontend/dist
```

Upload isi folder tersebut ke domain frontend hosting:

```text
/home/wurdgtgl/anisaaaaa.sbs
```

## 4. Dokumentasi Web

Dokumen yang tampil di halaman `/dokumentasi` berada di:

```text
frontend/public/docs
```

Jika mengubah dokumentasi, jalankan build ulang lalu upload `dist` lagi.

## 5. Route Penting

- `/` dashboard utama
- `/dokumentasi` daftar dokumentasi
- `/dokumentasi/penggunaan_sistem`
- `/dokumentasi/kebutuhan_sistem`
- `/dokumentasi/deployment_production`
- `/dokumentasi/api_backend`
- `/dokumentasi/diagram_skripsi`

## 6. Catatan Hosting

Karena frontend memakai React SPA, `.htaccess` domain frontend harus mengarahkan route yang tidak berupa file ke `index.html`.
