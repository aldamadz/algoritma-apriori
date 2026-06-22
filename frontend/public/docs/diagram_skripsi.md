# Diagram Skripsi - Sistem Analisis Pola Peminjaman Perpustakaan

Dokumen ini berisi diagram yang relevan dengan implementasi sistem Apriori Engine.

## 1. Entity Diagram Konseptual

```mermaid
erDiagram
  DEPARTMENT ||--o{ STUDENT : memiliki
  STUDENT ||--o{ LOAN_TRANSACTION : melakukan
  LOAN_TRANSACTION ||--o{ LOAN_TRANSACTION_ITEM : berisi
  BOOK ||--o{ LOAN_TRANSACTION_ITEM : dipinjam
  ANALYSIS_RUN ||--o{ ASSOCIATION_RULE : menghasilkan
```

## 2. ERD Logical

```mermaid
erDiagram
  DEPARTMENT {
    int id PK
    string code UK
    string name
    datetime created_at
  }

  STUDENT {
    int id PK
    string student_number UK
    string name
    int department_id FK
    datetime created_at
  }

  BOOK {
    int id PK
    string isbn UK
    string title
    string author
    string category
    datetime created_at
  }

  LOAN_TRANSACTION {
    int id PK
    int student_id FK
    date loan_date
    date return_date
    datetime created_at
  }

  LOAN_TRANSACTION_ITEM {
    int id PK
    int transaction_id FK
    int book_id FK
  }

  ANALYSIS_RUN {
    int id PK
    string run_name
    date period_start
    date period_end
    float min_support
    float min_confidence
    float min_lift
    string status
    datetime created_at
    datetime finished_at
  }

  ASSOCIATION_RULE {
    int id PK
    int analysis_run_id FK
    json antecedent_items
    json consequent_items
    text antecedent_text
    text consequent_text
    float support_value
    float confidence_value
    float lift_value
    int support_count
    datetime created_at
  }

  DEPARTMENT ||--o{ STUDENT : "1..n"
  STUDENT ||--o{ LOAN_TRANSACTION : "1..n"
  LOAN_TRANSACTION ||--o{ LOAN_TRANSACTION_ITEM : "1..n"
  BOOK ||--o{ LOAN_TRANSACTION_ITEM : "1..n"
  ANALYSIS_RUN ||--o{ ASSOCIATION_RULE : "1..n"
```

## 3. Use Case Diagram

```mermaid
flowchart LR
  A[Admin atau Operator] --> UC1[Import CSV Transaksi]
  A --> UC2[Kosongkan Dataset]
  A --> UC3[Jalankan Analisis Apriori]
  A --> UC4[Lihat Riwayat Run]
  A --> UC5[Lihat Rules]
  A --> UC6[Bandingkan 2 Run]
  A --> UC7[Hapus Run]
  A --> UC8[Lihat Dokumentasi Sistem]
```

## 4. Flowchart End-to-End

```mermaid
flowchart TD
  S([Start]) --> U[Upload CSV]
  U --> V{Format CSV valid?}
  V -- Tidak --> E[Tampilkan error validasi]
  E --> U
  V -- Ya --> P[Preprocessing data]
  P --> M[Simpan master dan transaksi]
  M --> A[Input parameter analisis]
  A --> R[Run Apriori]
  R --> G[Hitung frequent itemset dan rules]
  G --> D[Simpan analysis run dan association rules]
  D --> T[Tampilkan rules di UI]
  T --> X([Selesai])
```

## 5. Activity Diagram Jalankan Analisis

```mermaid
flowchart TD
  A[User membuka panel Jalankan Analisis] --> B[Isi support confidence lift]
  B --> C[Klik tombol Run]
  C --> D[Backend mengambil transaksi]
  D --> E[Membentuk basket Fakultas dan Buku]
  E --> F[Apriori mencari frequent itemset]
  F --> G[Generate association rules]
  G --> H[Filter rules sesuai threshold]
  H --> I[Simpan hasil ke database]
  I --> J[Frontend refresh riwayat dan rules]
```

## 6. Sequence Diagram Import CSV

```mermaid
sequenceDiagram
  participant U as User
  participant FE as Frontend
  participant API as FastAPI
  participant DB as PostgreSQL

  U->>FE: Pilih file CSV dan klik Import
  FE->>API: POST /api/transactions/import-csv
  API->>API: Validasi kolom dan parsing CSV
  API->>API: Normalisasi fakultas, mahasiswa, buku, tanggal
  API->>DB: Upsert departments, students, books
  API->>DB: Insert loan_transactions dan loan_transaction_items
  DB-->>API: Data tersimpan
  API-->>FE: Summary import
  FE-->>U: Tampilkan hasil import
```

## 7. Sequence Diagram Run Apriori

```mermaid
sequenceDiagram
  participant U as User
  participant FE as Frontend
  participant API as FastAPI
  participant ENG as Apriori Engine
  participant DB as PostgreSQL

  U->>FE: Klik Jalankan Analisis
  FE->>API: POST /api/analysis/run
  API->>DB: Ambil transaksi beserta buku dan fakultas
  API->>ENG: Kirim basket dan parameter
  ENG-->>API: Rules support confidence lift
  API->>DB: Simpan analysis_runs dan association_rules
  API-->>FE: Status done
  FE->>API: GET /api/analysis/runs/{id}/rules
  API-->>FE: Rules dan summary
```

## 8. Deployment Diagram Production

```mermaid
flowchart LR
  U[Browser User] --> FE[anisaaaaa.sbs - Static React]
  FE --> API[api.anisaaaaa.sbs - FastAPI via Passenger WSGI]
  API --> DB[(PostgreSQL Hosting)]
```

## 9. Arsitektur Komponen

```mermaid
flowchart LR
  subgraph Frontend
    A1[Import CSV Panel]
    A2[Run Analysis Panel]
    A3[Master Data Panel]
    A4[Runs History Panel]
    A5[Compare Runs Panel]
    A6[Rules Table dan Detail]
    A7[Documentation Page]
  end

  subgraph Backend
    B1[Transactions Route]
    B2[Analysis Route]
    B3[Students Route]
    B4[Books Route]
    B5[Departments Route]
    B6[Apriori Engine Service]
  end

  subgraph Database
    C1[(departments)]
    C2[(students)]
    C3[(books)]
    C4[(loan_transactions)]
    C5[(loan_transaction_items)]
    C6[(analysis_runs)]
    C7[(association_rules)]
  end

  A1 --> B1
  A2 --> B2
  A3 --> B3
  A3 --> B4
  A3 --> B1
  A4 --> B2
  A5 --> B2
  A6 --> B2
  B2 --> B6
  B1 --> C1
  B1 --> C2
  B1 --> C3
  B1 --> C4
  B1 --> C5
  B2 --> C6
  B2 --> C7
```

## 10. Catatan untuk Laporan

- Entity Diagram dan ERD dapat digunakan pada bagian perancangan basis data.
- Use Case, Activity, Sequence, dan Flowchart dapat digunakan pada bagian perancangan sistem.
- Deployment Diagram dapat digunakan pada bagian implementasi.
- Jika laporan membutuhkan gambar statis, gunakan PNG yang sudah tersedia pada halaman dokumentasi.
