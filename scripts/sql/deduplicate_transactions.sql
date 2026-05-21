-- Menghapus transaksi peminjaman duplikat.
-- Duplikat didefinisikan sebagai:
-- mahasiswa sama + tanggal pinjam sama + tanggal kembali sama + daftar buku sama.
-- Transaksi dengan id paling kecil dipertahankan, sisanya dihapus.

BEGIN;

WITH transaction_signatures AS (
  SELECT
    lt.id,
    lt.student_id,
    lt.loan_date,
    lt.return_date,
    array_agg(lti.book_id ORDER BY lti.book_id) AS book_ids
  FROM loan_transactions lt
  JOIN loan_transaction_items lti ON lti.transaction_id = lt.id
  GROUP BY lt.id, lt.student_id, lt.loan_date, lt.return_date
),
ranked_duplicates AS (
  SELECT
    id,
    row_number() OVER (
      PARTITION BY student_id, loan_date, return_date, book_ids
      ORDER BY id
    ) AS duplicate_rank
  FROM transaction_signatures
),
deleted_transactions AS (
  DELETE FROM loan_transactions
  WHERE id IN (
    SELECT id
    FROM ranked_duplicates
    WHERE duplicate_rank > 1
  )
  RETURNING id
)
SELECT count(*) AS deleted_duplicate_transactions
FROM deleted_transactions;

COMMIT;

