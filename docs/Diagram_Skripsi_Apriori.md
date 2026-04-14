# Diagram Skripsi - Sistem Analisis Pola Peminjaman Perpustakaan

Dokumen ini berisi kumpulan diagram untuk kebutuhan skripsi berbasis implementasi sistem yang sudah berjalan.

## 1. Entity Diagram (Konseptual)

```mermaid
erDiagram
  DEPARTMENT ||--o{ STUDENT : memiliki
  STUDENT ||--o{ LOAN_TRANSACTION : melakukan
  LOAN_TRANSACTION ||--o{ LOAN_TRANSACTION_ITEM : berisi
  BOOK ||--o{ LOAN_TRANSACTION_ITEM : dipinjam
  ANALYSIS_RUN ||--o{ ASSOCIATION_RULE : menghasilkan
```

## 2. ERD (Logical + Atribut)

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
  A[Admin/Operator] --> UC1[Import CSV Transaksi]
  A --> UC2[Jalankan Analisis Apriori]
  A --> UC3[Lihat Riwayat Run]
  A --> UC4[Lihat Rules]
  A --> UC5[Bandingkan 2 Run]
  A --> UC6[Hapus Run]
  A --> UC7[Lihat Dokumentasi Sistem]
```

## 4. Flowchart Proses Sistem (End-to-End)

```mermaid
flowchart TD
  S([Start]) --> U[Upload CSV]
  U --> V{Validasi format & kolom}
  V -- Tidak valid --> E1[Catat error baris]
  E1 --> U
  V -- Valid --> M[Simpan master & transaksi]
  M --> P[Input parameter min_support, min_confidence, min_lift]
  P --> R[Run Apriori]
  R --> G[Generate rules + hitung support/confidence/lift]
  G --> D[Simpan ke analysis_runs & association_rules]
  D --> T[Tampilkan rules di UI]
  T --> C{Perlu compare run?}
  C -- Ya --> K[Bandingkan Run A vs Run B]
  C -- Tidak --> X([Selesai])
  K --> X
```

## 5. Activity Diagram (Jalankan Analisis)

```mermaid
flowchart TD
  A[User pilih menu Jalankan Analisis] --> B[Isi parameter]
  B --> C[Klik Run]
  C --> D[Backend ambil transaksi]
  D --> E[Bentuk basket Jurusan + Buku]
  E --> F[Frequent Itemset Mining]
  F --> G[Association Rule Generation]
  G --> H[Simpan hasil run]
  H --> I[UI reload run terbaru]
  I --> J[Rules ditampilkan]
```

## 6. Sequence Diagram (Import CSV)

```mermaid
sequenceDiagram
  participant U as User
  participant FE as Frontend
  participant API as FastAPI
  participant DB as PostgreSQL/SQLite

  U->>FE: Pilih file CSV + klik Import
  FE->>API: POST /api/transactions/import-csv (multipart)
  API->>API: Validasi kolom + parsing row
  API->>DB: Upsert Department/Student/Book
  API->>DB: Insert LoanTransaction + LoanTransactionItem
  DB-->>API: OK
  API-->>FE: Summary import + errors
  FE-->>U: Tampilkan hasil import
```

## 7. Sequence Diagram (Run Apriori)

```mermaid
sequenceDiagram
  participant U as User
  participant FE as Frontend
  participant API as FastAPI
  participant ENG as Apriori Engine
  participant DB as PostgreSQL/SQLite

  U->>FE: Klik Run Analysis
  FE->>API: POST /api/analysis/run
  API->>DB: Ambil transaksi + relasi buku/jurusan
  API->>ENG: Kirim basket + parameter
  ENG-->>API: Rules (support, confidence, lift)
  API->>DB: Simpan analysis_run + association_rules
  API-->>FE: Response status done
  FE->>API: GET /api/analysis/runs/{id}/rules
  API-->>FE: Data rules + summary
```

## 8. Deployment Diagram

```mermaid
flowchart LR
  U[Browser User] --> CF[Cloudflare Tunnel]
  CF --> NGINX[Nginx Frontend Container :18080]
  NGINX --> FE[Static React App]
  NGINX --> API[FastAPI Container :18000 via /api]
  API --> DB[(PostgreSQL Existing Container)]
```

## 9. Arsitektur Komponen (Aplikasi)

```mermaid
flowchart LR
  subgraph Frontend
    A1[Import CSV Panel]
    A2[Run Analysis Panel]
    A3[Runs History Panel]
    A4[Compare Runs Panel]
    A5[Rules Table + Filter + Detail]
  end

  subgraph Backend
    B1[Transactions Route]
    B2[Analysis Route]
    B3[Apriori Engine Service]
  end

  subgraph Data
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
  A3 --> B2
  A4 --> B2
  A5 --> B2
  B2 --> B3
  B1 --> C1
  B1 --> C2
  B1 --> C3
  B1 --> C4
  B1 --> C5
  B2 --> C6
  B2 --> C7
```

## 10. Catatan untuk Laporan Skripsi

- Gunakan ERD pada Bab Perancangan Basis Data.
- Gunakan Flowchart/Activity/Sequence pada Bab Perancangan Sistem.
- Gunakan Deployment dan Arsitektur Komponen pada Bab Implementasi.
- Jika kampus mewajibkan gambar statis, render Mermaid ke PNG/SVG sebelum dimasukkan ke dokumen.
