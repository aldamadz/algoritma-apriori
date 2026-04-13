from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import Department
from app.schemas.common import DepartmentCreate, DepartmentOut

router = APIRouter()


@router.get("", response_model=list[DepartmentOut])
def list_departments(db: Session = Depends(get_db)) -> list[Department]:
    return list(db.scalars(select(Department).order_by(Department.name)))


@router.post("", response_model=DepartmentOut, status_code=status.HTTP_201_CREATED)
def create_department(payload: DepartmentCreate, db: Session = Depends(get_db)) -> Department:
    exists = db.scalar(
        select(Department).where((Department.code == payload.code) | (Department.name == payload.name))
    )
    if exists:
        raise HTTPException(status_code=409, detail="Department already exists.")
    department = Department(code=payload.code.strip(), name=payload.name.strip())
    db.add(department)
    db.commit()
    db.refresh(department)
    return department
