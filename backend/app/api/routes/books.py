from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import Book
from app.schemas.common import BookCreate, BookOut, PaginatedBooksResponse, RulesMeta

router = APIRouter()


@router.get("", response_model=PaginatedBooksResponse)
def list_books(
    db: Session = Depends(get_db),
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=20, ge=1, le=100),
    q: str | None = None,
) -> PaginatedBooksResponse:
    base_stmt = select(Book)
    count_stmt = select(func.count(Book.id))
    if q:
        pattern = f"%{q}%"
        condition = or_(
            Book.isbn.ilike(pattern),
            Book.title.ilike(pattern),
            Book.category.ilike(pattern),
        )
        base_stmt = base_stmt.where(condition)
        count_stmt = count_stmt.where(condition)

    total = int(db.scalar(count_stmt) or 0)
    total_pages = max(1, (total + limit - 1) // limit)
    rows = list(
        db.scalars(
            base_stmt
            .order_by(Book.title)
            .offset((page - 1) * limit)
            .limit(limit)
        )
    )
    return PaginatedBooksResponse(
        data=[BookOut.model_validate(row) for row in rows],
        meta=RulesMeta(page=page, limit=limit, total=total, totalPages=total_pages),
    )


@router.post("", response_model=BookOut, status_code=status.HTTP_201_CREATED)
def create_book(payload: BookCreate, db: Session = Depends(get_db)) -> Book:
    exists = db.scalar(select(Book).where((Book.isbn == payload.isbn) | (Book.title == payload.title)))
    if exists:
        raise HTTPException(status_code=409, detail="Book already exists.")
    book = Book(
        isbn=payload.isbn.strip(),
        title=payload.title.strip(),
        author=payload.author.strip(),
        category=payload.category.strip(),
    )
    db.add(book)
    db.commit()
    db.refresh(book)
    return book
