from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session, joinedload

from app.db.session import get_db
from app.models import Department, Student
from app.schemas.common import PaginatedStudentsResponse, RulesMeta, StudentCreate, StudentOut

router = APIRouter()


@router.get("", response_model=PaginatedStudentsResponse)
def list_students(
    db: Session = Depends(get_db),
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=20, ge=1, le=100),
    q: str | None = None,
) -> PaginatedStudentsResponse:
    base_stmt = select(Student).join(Student.department)
    count_stmt = select(func.count(Student.id)).select_from(Student).join(Student.department)
    if q:
        pattern = f"%{q}%"
        condition = or_(
            Student.student_number.ilike(pattern),
            Student.name.ilike(pattern),
            Department.name.ilike(pattern),
        )
        base_stmt = base_stmt.where(condition)
        count_stmt = count_stmt.where(condition)

    total = int(db.scalar(count_stmt) or 0)
    total_pages = max(1, (total + limit - 1) // limit)
    rows = list(
        db.scalars(
            base_stmt
            .options(joinedload(Student.department))
            .order_by(Student.name)
            .offset((page - 1) * limit)
            .limit(limit)
        )
    )
    data = [
        StudentOut(
            id=row.id,
            student_number=row.student_number,
            name=row.name,
            department_id=row.department_id,
            department_name=row.department.name if row.department else None,
        )
        for row in rows
    ]
    return PaginatedStudentsResponse(
        data=data,
        meta=RulesMeta(page=page, limit=limit, total=total, totalPages=total_pages),
    )


@router.post("", response_model=StudentOut, status_code=status.HTTP_201_CREATED)
def create_student(payload: StudentCreate, db: Session = Depends(get_db)) -> Student:
    department = db.get(Department, payload.department_id)
    if not department:
        raise HTTPException(status_code=404, detail="Department not found.")
    exists = db.scalar(select(Student).where(Student.student_number == payload.student_number))
    if exists:
        raise HTTPException(status_code=409, detail="Student number already exists.")
    student = Student(
        student_number=payload.student_number.strip(),
        name=payload.name.strip(),
        department_id=payload.department_id,
    )
    db.add(student)
    db.commit()
    db.refresh(student)
    return student
