from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import Department, Student
from app.schemas.common import StudentCreate, StudentOut

router = APIRouter()


@router.get("", response_model=list[StudentOut])
def list_students(db: Session = Depends(get_db)) -> list[Student]:
    return list(db.scalars(select(Student).order_by(Student.name)))


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
