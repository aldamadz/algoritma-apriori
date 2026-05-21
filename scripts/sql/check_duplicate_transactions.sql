-- Mengecek transaksi peminjaman duplikat tanpa menghapus data.
-- Duplikat didefinisikan sebagai:
-- mahasiswa sama + tanggal pinjam sama + tanggal kembali sama + daftar buku sama.

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
duplicate_groups AS (
  SELECT
    student_id,
    loan_date,
    return_date,
    book_ids,
    count(*) AS duplicate_count,
    min(id) AS kept_transaction_id,
    array_agg(id ORDER BY id) AS transaction_ids
  FROM transaction_signatures
  GROUP BY student_id, loan_date, return_date, book_ids
  HAVING count(*) > 1
)
SELECT
  count(*) AS duplicate_groups,
  coalesce(sum(duplicate_count - 1), 0) AS deletable_duplicate_transactions
FROM duplicate_groups;

