import csv
import io
from datetime import date

from fastapi import APIRouter, Depends, File, Header, HTTPException, Query, UploadFile, status
from sqlalchemy import delete, func, select
from sqlalchemy import or_
from sqlalchemy.orm import Session, joinedload

from app.db.session import get_db
from app.models import (
    AnalysisRun,
    AssociationRule,
    Book,
    Department,
    LoanTransaction,
    LoanTransactionItem,
    Student,
)
from app.schemas.common import (
    ImportCsvResult,
    LoanTransactionCreate,
    LoanTransactionOut,
    PaginatedTransactionsResponse,
    ResetDataResult,
    RulesMeta,
    TransactionSummaryResponse,
)

router = APIRouter()


STANDARD_REQUIRED_COLUMNS = ["transaction_id", "student_number", "department_code", "loan_date", "book_isbn"]
REAL_LIBRARY_REQUIRED_COLUMNS = ["no_mhs", "nama", "fakultas", "kd_buku", "judul", "tgl_pinjam"]


def _cell(row: dict[str, str], key: str) -> str:
    return (row.get(key) or "").strip()


def _department_code(value: str) -> str:
    code = "".join(ch for ch in value.upper() if ch.isalnum())
    return (code or "UNKNOWN")[:30]


def _detect_csv_format(headers: list[str]) -> str:
    if all(column in headers for column in STANDARD_REQUIRED_COLUMNS):
        return "standard"
    if all(column in headers for column in REAL_LIBRARY_REQUIRED_COLUMNS):
        return "real_library"

    standard_missing = [c for c in STANDARD_REQUIRED_COLUMNS if c not in headers]
    real_missing = [c for c in REAL_LIBRARY_REQUIRED_COLUMNS if c not in headers]
    raise HTTPException(
        status_code=400,
        detail=(
            "Unsupported CSV columns. "
            f"Standard missing: {', '.join(standard_missing)}. "
            f"Real library missing: {', '.join(real_missing)}."
        ),
    )


def _normalize_import_rows(rows: list[dict[str, str]], csv_format: str) -> list[dict[str, str]]:
    if csv_format == "standard":
        return rows

    normalized: list[dict[str, str]] = []
    for row in rows:
        student_number = _cell(row, "no_mhs")
        loan_date = _cell(row, "tgl_pinjam")
        return_date = _cell(row, "tgl_kembali")
        department_name = _cell(row, "fakultas") or "Unknown"
        book_isbn = _cell(row, "kd_buku") or _cell(row, "no_barcode")

        normalized.append(
            {
                "transaction_id": f"{student_number}|{loan_date}|{return_date}",
                "student_number": student_number,
                "student_name": _cell(row, "nama") or student_number or "Unknown",
                "department_code": _department_code(department_name),
                "department_name": department_name,
                "loan_date": loan_date,
                "return_date": return_date,
                "book_isbn": book_isbn,
                "book_title": _cell(row, "judul") or book_isbn,
                "book_author": "",
                "book_category": _cell(row, "label2") or _cell(row, "label1"),
            }
        )
    return normalized


@router.get("/summary", response_model=TransactionSummaryResponse)
def get_transaction_summary(db: Session = Depends(get_db)) -> TransactionSummaryResponse:
    first_loan_date, last_loan_date, total_transactions = db.execute(
        select(
            func.min(LoanTransaction.loan_date),
            func.max(LoanTransaction.loan_date),
            func.count(LoanTransaction.id),
        )
    ).one()

    month_label = func.to_char(LoanTransaction.loan_date, "YYYY-MM")
    monthly_rows = db.execute(
        select(
            month_label.label("month"),
            func.count(LoanTransaction.id).label("total"),
        )
        .group_by(month_label)
        .order_by(month_label)
    ).all()

    return TransactionSummaryResponse(
        firstLoanDate=first_loan_date,
        lastLoanDate=last_loan_date,
        totalTransactions=int(total_transactions or 0),
        monthly=[{"month": month, "total": int(total)} for month, total in monthly_rows],
    )


@router.delete("/all-data", response_model=ResetDataResult)
def reset_all_data(
    x_confirm_reset: str | None = Header(default=None),
    db: Session = Depends(get_db),
) -> ResetDataResult:
    if x_confirm_reset != "RESET ALL DATA":
        raise HTTPException(status_code=400, detail="Reset confirmation is required.")

    counts = {
        "deletedRules": int(db.scalar(select(func.count(AssociationRule.id))) or 0),
        "deletedAnalysisRuns": int(db.scalar(select(func.count(AnalysisRun.id))) or 0),
        "deletedTransactionItems": int(
            db.scalar(select(func.count(LoanTransactionItem.id))) or 0
        ),
        "deletedTransactions": int(db.scalar(select(func.count(LoanTransaction.id))) or 0),
        "deletedBooks": int(db.scalar(select(func.count(Book.id))) or 0),
        "deletedStudents": int(db.scalar(select(func.count(Student.id))) or 0),
        "deletedDepartments": int(db.scalar(select(func.count(Department.id))) or 0),
    }

    try:
        for model in (
            AssociationRule,
            AnalysisRun,
            LoanTransactionItem,
            LoanTransaction,
            Book,
            Student,
            Department,
        ):
            db.execute(delete(model))
        db.commit()
    except Exception:
        db.rollback()
        raise

    return ResetDataResult(**counts)


@router.get("", response_model=PaginatedTransactionsResponse)
def list_transactions(
    db: Session = Depends(get_db),
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=20, ge=1, le=100),
    q: str | None = None,
) -> PaginatedTransactionsResponse:
    base_stmt = select(LoanTransaction).join(LoanTransaction.student).join(Student.department)
    count_stmt = select(func.count(func.distinct(LoanTransaction.id))).select_from(LoanTransaction).join(LoanTransaction.student).join(Student.department)
    if q:
        pattern = f"%{q}%"
        base_stmt = base_stmt.join(LoanTransaction.items).join(LoanTransactionItem.book)
        count_stmt = count_stmt.join(LoanTransaction.items).join(LoanTransactionItem.book)
        condition = or_(
            Student.student_number.ilike(pattern),
            Student.name.ilike(pattern),
            Department.name.ilike(pattern),
            Book.title.ilike(pattern),
        )
        base_stmt = base_stmt.where(condition)
        count_stmt = count_stmt.where(condition)

    total = int(db.scalar(count_stmt) or 0)
    total_pages = max(1, (total + limit - 1) // limit)
    rows = (
        db.execute(
            base_stmt
            .options(
                joinedload(LoanTransaction.student).joinedload(Student.department),
                joinedload(LoanTransaction.items).joinedload(LoanTransactionItem.book),
            )
            .order_by(LoanTransaction.loan_date.desc(), LoanTransaction.id.desc())
            .offset((page - 1) * limit)
            .limit(limit)
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
                student_number=row.student.student_number if row.student else None,
                student_name=row.student.name if row.student else None,
                department_name=row.student.department.name if row.student and row.student.department else None,
                loan_date=row.loan_date,
                return_date=row.return_date,
                book_ids=[item.book_id for item in row.items],
                book_titles=[item.book.title for item in row.items if item.book],
            )
        )
    return PaginatedTransactionsResponse(
        data=out,
        meta=RulesMeta(page=page, limit=limit, total=total, totalPages=total_pages),
    )


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
        student_number=row.student.student_number if row.student else None,
        student_name=row.student.name if row.student else None,
        department_name=row.student.department.name if row.student and row.student.department else None,
        loan_date=row.loan_date,
        return_date=row.return_date,
        book_ids=[item.book_id for item in row.items],
        book_titles=[item.book.title for item in row.items if item.book],
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
    headers = reader.fieldnames or []
    csv_format = _detect_csv_format(headers)

    source_rows = list(reader)
    rows = _normalize_import_rows(source_rows, csv_format)
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
    skipped_duplicate_transactions = 0
    removed_duplicate_transactions = 0
    errors: list[str] = []

    for txn_id, group_rows in grouped.items():
        first = group_rows[0]
        student_number = (first.get("student_number") or "").strip()
        department_code = (first.get("department_code") or "").strip()
        loan_date_raw = (first.get("loan_date") or "").strip()
        return_date_raw = (first.get("return_date") or "").strip()
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
        return_date_value: date | None = None
        if return_date_raw:
            try:
                return_date_value = date.fromisoformat(return_date_raw)
            except ValueError:
                errors.append(f"transaction_id={txn_id}: invalid return_date '{return_date_raw}', expected YYYY-MM-DD")

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

        books_by_id: dict[int, Book] = {}
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

            books_by_id[book.id] = book

        if not books_by_id:
            errors.append(f"transaction_id={txn_id}: no valid books")
            continue

        existing_transactions = (
            db.execute(
                select(LoanTransaction)
                .options(joinedload(LoanTransaction.items))
                .where(
                    LoanTransaction.student_id == student.id,
                    LoanTransaction.loan_date == loan_date_value,
                    LoanTransaction.return_date == return_date_value,
                )
            )
            .unique()
            .scalars()
            .all()
        )
        imported_book_ids = set(books_by_id)
        matching_transactions = [
            existing
            for existing in existing_transactions
            if {item.book_id for item in existing.items} == imported_book_ids
        ]
        if matching_transactions:
            for duplicate in matching_transactions[1:]:
                db.delete(duplicate)
                removed_duplicate_transactions += 1
            skipped_duplicate_transactions += 1
            continue

        transaction = LoanTransaction(
            student_id=student.id,
            loan_date=loan_date_value,
            return_date=return_date_value,
        )
        db.add(transaction)
        db.flush()
        created_transactions += 1

        for book_id in imported_book_ids:
            db.add(LoanTransactionItem(transaction_id=transaction.id, book_id=book_id))
            created_items += 1

    db.commit()

    return ImportCsvResult(
        totalRows=len(source_rows),
        createdTransactions=created_transactions,
        createdTransactionItems=created_items,
        createdDepartments=created_departments,
        createdStudents=created_students,
        createdBooks=created_books,
        skippedDuplicateTransactions=skipped_duplicate_transactions,
        removedDuplicateTransactions=removed_duplicate_transactions,
        errors=errors,
    )
