from datetime import date, datetime
from pydantic import BaseModel, Field


class DepartmentCreate(BaseModel):
    code: str = Field(min_length=1, max_length=30)
    name: str = Field(min_length=1, max_length=120)


class DepartmentOut(BaseModel):
    id: int
    code: str
    name: str

    class Config:
        from_attributes = True


class StudentCreate(BaseModel):
    student_number: str
    name: str
    department_id: int


class StudentOut(BaseModel):
    id: int
    student_number: str
    name: str
    department_id: int

    class Config:
        from_attributes = True


class BookCreate(BaseModel):
    isbn: str
    title: str
    author: str = ""
    category: str = ""


class BookOut(BaseModel):
    id: int
    isbn: str
    title: str
    author: str
    category: str

    class Config:
        from_attributes = True


class LoanTransactionCreate(BaseModel):
    student_id: int
    loan_date: date
    return_date: date | None = None
    book_ids: list[int] = Field(default_factory=list, min_length=1)


class LoanTransactionOut(BaseModel):
    id: int
    student_id: int
    loan_date: date
    return_date: date | None
    book_ids: list[int]


class ImportCsvResult(BaseModel):
    totalRows: int
    createdTransactions: int
    createdTransactionItems: int
    createdDepartments: int
    createdStudents: int
    createdBooks: int
    errors: list[str]


class AnalysisRunCreate(BaseModel):
    run_name: str = "manual-run"
    period_start: date | None = None
    period_end: date | None = None
    min_support: float = Field(gt=0, le=1)
    min_confidence: float = Field(gt=0, le=1)
    min_lift: float = Field(ge=0, default=0)


class AnalysisRunOut(BaseModel):
    id: int
    run_name: str
    period_start: date | None
    period_end: date | None
    min_support: float
    min_confidence: float
    min_lift: float
    status: str
    created_at: datetime
    finished_at: datetime | None

    class Config:
        from_attributes = True


class RuleOut(BaseModel):
    id: int
    antecedent: list[str]
    consequent: list[str]
    support: float
    confidence: float
    lift: float
    supportCount: int


class RulesMeta(BaseModel):
    page: int
    limit: int
    total: int
    totalPages: int


class RulesSummary(BaseModel):
    totalRules: int
    topLiftRule: RuleOut | None = None
    dominantDepartment: str | None = None


class RulesResponse(BaseModel):
    data: list[RuleOut]
    meta: RulesMeta
    summary: RulesSummary
