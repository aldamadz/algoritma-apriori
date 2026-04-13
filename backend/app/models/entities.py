from datetime import date, datetime

from sqlalchemy import Date, DateTime, Float, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import JSON

from app.db.base import Base


def JsonType():
    # Fallback ke JSON untuk DB selain PostgreSQL.
    return JSON().with_variant(JSONB, "postgresql")


class Department(Base):
    __tablename__ = "departments"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    code: Mapped[str] = mapped_column(String(30), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(120), unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    students: Mapped[list["Student"]] = relationship(back_populates="department")


class Student(Base):
    __tablename__ = "students"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    student_number: Mapped[str] = mapped_column(String(40), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(150))
    department_id: Mapped[int] = mapped_column(ForeignKey("departments.id", ondelete="RESTRICT"))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    department: Mapped["Department"] = relationship(back_populates="students")
    transactions: Mapped[list["LoanTransaction"]] = relationship(back_populates="student")


class Book(Base):
    __tablename__ = "books"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    isbn: Mapped[str] = mapped_column(String(40), unique=True, index=True)
    title: Mapped[str] = mapped_column(String(255), index=True)
    author: Mapped[str] = mapped_column(String(150), default="")
    category: Mapped[str] = mapped_column(String(120), default="")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    items: Mapped[list["LoanTransactionItem"]] = relationship(back_populates="book")


class LoanTransaction(Base):
    __tablename__ = "loan_transactions"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id", ondelete="RESTRICT"), index=True)
    loan_date: Mapped[date] = mapped_column(Date, index=True)
    return_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    student: Mapped["Student"] = relationship(back_populates="transactions")
    items: Mapped[list["LoanTransactionItem"]] = relationship(back_populates="transaction", cascade="all, delete-orphan")


class LoanTransactionItem(Base):
    __tablename__ = "loan_transaction_items"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    transaction_id: Mapped[int] = mapped_column(ForeignKey("loan_transactions.id", ondelete="CASCADE"), index=True)
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id", ondelete="RESTRICT"), index=True)

    transaction: Mapped["LoanTransaction"] = relationship(back_populates="items")
    book: Mapped["Book"] = relationship(back_populates="items")


class AnalysisRun(Base):
    __tablename__ = "analysis_runs"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    run_name: Mapped[str] = mapped_column(String(120), index=True)
    period_start: Mapped[date | None] = mapped_column(Date, nullable=True)
    period_end: Mapped[date | None] = mapped_column(Date, nullable=True)
    min_support: Mapped[float] = mapped_column(Float)
    min_confidence: Mapped[float] = mapped_column(Float)
    min_lift: Mapped[float] = mapped_column(Float, default=0.0)
    status: Mapped[str] = mapped_column(String(20), default="done")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    rules: Mapped[list["AssociationRule"]] = relationship(
        back_populates="analysis_run", cascade="all, delete-orphan"
    )


class AssociationRule(Base):
    __tablename__ = "association_rules"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    analysis_run_id: Mapped[int] = mapped_column(ForeignKey("analysis_runs.id", ondelete="CASCADE"), index=True)
    antecedent_items: Mapped[list[str]] = mapped_column(JsonType())
    consequent_items: Mapped[list[str]] = mapped_column(JsonType())
    antecedent_text: Mapped[str] = mapped_column(Text)
    consequent_text: Mapped[str] = mapped_column(Text)
    support_value: Mapped[float] = mapped_column(Float, index=True)
    confidence_value: Mapped[float] = mapped_column(Float, index=True)
    lift_value: Mapped[float] = mapped_column(Float, index=True)
    support_count: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    analysis_run: Mapped["AnalysisRun"] = relationship(back_populates="rules")
