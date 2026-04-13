import csv
import io
from datetime import date

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.db.session import get_db
from app.models import Book, Department, LoanTransaction, LoanTransactionItem, Student
from app.schemas.common import ImportCsvResult, LoanTransactionCreate, LoanTransactionOut

router = APIRouter()


@router.get("", response_model=list[LoanTransactionOut])
def list_transactions(db: Session = Depends(get_db)) -> list[LoanTransactionOut]:
    rows = (
        db.execute(
        select(LoanTransaction)
        .options(joinedload(LoanTransaction.items))
        .order_by(LoanTransaction.loan_date.desc(), LoanTransaction.id.desc())
        )
        .unique()
        .scalars()
        .all()
    )
    out: list[LoanTransactionOut] = []
    for row in rows:
        out.append(
            LoanTransactionOut(
                id=row.id,
                student_id=row.student_id,
                loan_date=row.loan_date,
                return_date=row.return_date,
                book_ids=[item.book_id for item in row.items],
            )
        )
    return out


@router.post("", response_model=LoanTransactionOut, status_code=status.HTTP_201_CREATED)
def create_transaction(payload: LoanTransactionCreate, db: Session = Depends(get_db)) -> LoanTransactionOut:
    student = db.get(Student, payload.student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found.")

    books = list(db.scalars(select(Book).where(Book.id.in_(payload.book_ids))))
    if len(books) != len(set(payload.book_ids)):
        raise HTTPException(status_code=404, detail="Some books not found.")

    transaction = LoanTransaction(
        student_id=payload.student_id,
        loan_date=payload.loan_date,
        return_date=payload.return_date,
    )
    db.add(transaction)
    db.flush()

    for book_id in set(payload.book_ids):
        db.add(LoanTransactionItem(transaction_id=transaction.id, book_id=book_id))

    db.commit()
    db.refresh(transaction)
    row = (
        db.execute(
            select(LoanTransaction)
            .options(joinedload(LoanTransaction.items))
            .where(LoanTransaction.id == transaction.id)
        )
        .unique()
        .scalar_one_or_none()
    )
    assert row is not None
    return LoanTransactionOut(
        id=row.id,
        student_id=row.student_id,
        loan_date=row.loan_date,
        return_date=row.return_date,
        book_ids=[item.book_id for item in row.items],
    )


@router.post("/import-csv", response_model=ImportCsvResult, status_code=status.HTTP_201_CREATED)
async def import_csv(file: UploadFile = File(...), db: Session = Depends(get_db)) -> ImportCsvResult:
    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="File must be .csv")

    content = await file.read()
    try:
        decoded = content.decode("utf-8-sig")
    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="CSV must be UTF-8 encoded.")

    reader = csv.DictReader(io.StringIO(decoded))
    required = ["transaction_id", "student_number", "department_code", "loan_date", "book_isbn"]
    headers = reader.fieldnames or []
    missing = [c for c in required if c not in headers]
    if missing:
        raise HTTPException(status_code=400, detail=f"Missing required columns: {', '.join(missing)}")

    rows = list(reader)
    grouped: dict[str, list[dict[str, str]]] = {}
    for row in rows:
        txn_id = (row.get("transaction_id") or "").strip()
        if not txn_id:
            continue
        grouped.setdefault(txn_id, []).append(row)

    created_transactions = 0
    created_items = 0
    created_departments = 0
    created_students = 0
    created_books = 0
    errors: list[str] = []

    for txn_id, group_rows in grouped.items():
        first = group_rows[0]
        student_number = (first.get("student_number") or "").strip()
        department_code = (first.get("department_code") or "").strip()
        loan_date_raw = (first.get("loan_date") or "").strip()
        student_name = (first.get("student_name") or student_number or "Unknown").strip()
        department_name = (first.get("department_name") or department_code or "Unknown").strip()

        if not student_number or not department_code or not loan_date_raw:
            errors.append(f"transaction_id={txn_id}: missing student_number/department_code/loan_date")
            continue
        try:
            loan_date_value = date.fromisoformat(loan_date_raw)
        except ValueError:
            errors.append(f"transaction_id={txn_id}: invalid loan_date '{loan_date_raw}', expected YYYY-MM-DD")
            continue

        department = db.scalar(select(Department).where(Department.code == department_code))
        if not department:
            department = Department(code=department_code, name=department_name)
            db.add(department)
            db.flush()
            created_departments += 1

        student = db.scalar(select(Student).where(Student.student_number == student_number))
        if not student:
            student = Student(
                student_number=student_number,
                name=student_name,
                department_id=department.id,
            )
            db.add(student)
            db.flush()
            created_students += 1

        transaction = LoanTransaction(student_id=student.id, loan_date=loan_date_value)
        db.add(transaction)
        db.flush()
        created_transactions += 1

        seen_book_ids: set[int] = set()
        for row in group_rows:
            book_isbn = (row.get("book_isbn") or "").strip()
            if not book_isbn:
                errors.append(f"transaction_id={txn_id}: empty book_isbn")
                continue
            book_title = (row.get("book_title") or book_isbn).strip()
            book_author = (row.get("book_author") or "").strip()
            book_category = (row.get("book_category") or "").strip()

            book = db.scalar(select(Book).where(Book.isbn == book_isbn))
            if not book:
                book = Book(
                    isbn=book_isbn,
                    title=book_title,
                    author=book_author,
                    category=book_category,
                )
                db.add(book)
                db.flush()
                created_books += 1

            if book.id in seen_book_ids:
                continue
            seen_book_ids.add(book.id)
            db.add(LoanTransactionItem(transaction_id=transaction.id, book_id=book.id))
            created_items += 1

    db.commit()

    return ImportCsvResult(
        totalRows=len(rows),
        createdTransactions=created_transactions,
        createdTransactionItems=created_items,
        createdDepartments=created_departments,
        createdStudents=created_students,
        createdBooks=created_books,
        errors=errors,
    )
