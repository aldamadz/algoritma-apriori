from datetime import date

from sqlalchemy import select

from app.db.base import Base
from app.db.session import SessionLocal, engine
from app.models import Book, Department, LoanTransaction, LoanTransactionItem, Student


def run() -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        # Skip hanya jika transaksi sudah ada (bukan hanya department),
        # supaya kondisi data parsial tetap bisa diperbaiki dengan seed.
        if db.scalar(select(LoanTransaction.id).limit(1)):
            print("Seed skipped: transactions already exist.")
            return

        ti = db.scalar(select(Department).where(Department.code == "TI"))
        si = db.scalar(select(Department).where(Department.code == "SI"))
        if not ti:
            ti = Department(code="TI", name="Teknik Informatika")
            db.add(ti)
            db.flush()
        if not si:
            si = Department(code="SI", name="Sistem Informasi")
            db.add(si)
            db.flush()

        existing_students = {
            s.student_number: s
            for s in db.scalars(select(Student).where(Student.student_number.in_(["S001", "S002", "S003", "S004"])))
        }
        students = [
            existing_students.get("S001") or Student(student_number="S001", name="Andi", department_id=ti.id),
            existing_students.get("S002") or Student(student_number="S002", name="Budi", department_id=ti.id),
            existing_students.get("S003") or Student(student_number="S003", name="Cici", department_id=si.id),
            existing_students.get("S004") or Student(student_number="S004", name="Deni", department_id=si.id),
        ]
        for s in students:
            if s.id is None:
                db.add(s)
        db.flush()

        existing_books = {
            b.isbn: b
            for b in db.scalars(
                select(Book).where(Book.isbn.in_(["978-0001", "978-0002", "978-0003", "978-0004"]))
            )
        }
        books = [
            existing_books.get("978-0001") or Book(isbn="978-0001", title="AI Dasar", author="A", category="AI"),
            existing_books.get("978-0002") or Book(isbn="978-0002", title="Python Praktis", author="B", category="Programming"),
            existing_books.get("978-0003") or Book(isbn="978-0003", title="Database Dasar", author="C", category="Database"),
            existing_books.get("978-0004") or Book(isbn="978-0004", title="SQL Lanjutan", author="D", category="Database"),
        ]
        for b in books:
            if b.id is None:
                db.add(b)
        db.flush()

        book_map = {b.title: b.id for b in books}

        txns = [
            (students[0].id, ["AI Dasar", "Python Praktis"]),
            (students[1].id, ["AI Dasar"]),
            (students[2].id, ["Database Dasar", "SQL Lanjutan"]),
            (students[0].id, ["AI Dasar", "Database Dasar"]),
            (students[3].id, ["Database Dasar", "SQL Lanjutan"]),
            (students[1].id, ["AI Dasar", "Python Praktis"]),
        ]

        for student_id, titles in txns:
            txn = LoanTransaction(student_id=student_id, loan_date=date(2026, 4, 1))
            db.add(txn)
            db.flush()
            for title in titles:
                db.add(LoanTransactionItem(transaction_id=txn.id, book_id=book_map[title]))

        db.commit()
        print("Seed completed.")
    finally:
        db.close()


if __name__ == "__main__":
    run()
