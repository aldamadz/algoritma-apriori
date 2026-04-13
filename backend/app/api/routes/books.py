from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import Book
from app.schemas.common import BookCreate, BookOut

router = APIRouter()


@router.get("", response_model=list[BookOut])
def list_books(db: Session = Depends(get_db)) -> list[Book]:
    return list(db.scalars(select(Book).order_by(Book.title)))


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
