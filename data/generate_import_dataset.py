import argparse
import csv
import random
from datetime import date, timedelta
from pathlib import Path

random.seed(42)

headers = [
    "transaction_id",
    "student_number",
    "student_name",
    "department_code",
    "department_name",
    "loan_date",
    "book_isbn",
    "book_title",
    "book_author",
    "book_category",
]

departments = [
    ("TI", "Teknik Informatika"),
    ("SI", "Sistem Informasi"),
    ("MI", "Manajemen Informatika"),
    ("TE", "Teknik Elektro"),
]

books = [
    ("978-1001", "AI Dasar", "A. Wijaya", "AI"),
    ("978-1002", "Machine Learning Praktis", "B. Santoso", "AI"),
    ("978-1003", "Python untuk Data", "C. Putra", "Programming"),
    ("978-1004", "Basis Data Dasar", "D. Sari", "Database"),
    ("978-1005", "SQL Lanjutan", "E. Nugroho", "Database"),
    ("978-1006", "Statistika Terapan", "F. Lestari", "Math"),
    ("978-1007", "Data Mining Konsep", "G. Hidayat", "Data Mining"),
    ("978-1008", "Pemrograman Web", "H. Pratama", "Web"),
    ("978-1009", "Algoritma dan Struktur Data", "I. Wibowo", "CS"),
    ("978-1010", "Sistem Informasi Manajemen", "J. Utami", "IS"),
]

start = date(2025, 1, 1)
student_pool = [f"ST{n:05d}" for n in range(1, 451)]
names = [f"Mahasiswa_{n:03d}" for n in range(1, 451)]
sn_to_name = {student_pool[i]: names[i] for i in range(len(student_pool))}

rows = []
parser = argparse.ArgumentParser()
parser.add_argument("--transactions", type=int, default=1000)
parser.add_argument("--output", default="")
args = parser.parse_args()

tx_count = args.transactions
default_output = Path(rf"D:\Koding\algoritma apriori\data\dataset_import_{tx_count}_transaksi.csv")
output = Path(args.output) if args.output else default_output

for t in range(1, tx_count + 1):
    txid = f"TX{t:06d}"
    dept_code, dept_name = random.choice(departments)
    student_number = random.choice(student_pool)
    student_name = sn_to_name[student_number]
    loan_date = (start + timedelta(days=random.randint(0, 450))).isoformat()
    num_books = random.randint(1, 4)
    chosen = random.sample(books, num_books)
    for book in chosen:
        rows.append(
            [
                txid,
                student_number,
                student_name,
                dept_code,
                dept_name,
                loan_date,
                book[0],
                book[1],
                book[2],
                book[3],
            ]
        )

with output.open("w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(headers)
    writer.writerows(rows)

print(output)
print(f"transactions={tx_count}")
print(f"rows={len(rows) + 1}")
