from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query, status
from collections import Counter

from sqlalchemy import and_, func, or_, select
from sqlalchemy.orm import Session, joinedload

from app.db.session import get_db
from app.models import (
    AnalysisRun,
    AssociationRule,
    Department,
    LoanTransaction,
    LoanTransactionItem,
    Student,
)
from app.schemas.common import (
    AnalysisRunCreate,
    AnalysisRunOut,
    RuleOut,
    RulesMeta,
    RulesResponse,
    RulesSummary,
)
from app.services.apriori_engine import generate_association_rules, generate_frequent_itemsets

router = APIRouter()


def _to_rule_out(row: AssociationRule) -> RuleOut:
    return RuleOut(
        id=row.id,
        antecedent=row.antecedent_items,
        consequent=row.consequent_items,
        support=row.support_value,
        confidence=row.confidence_value,
        lift=row.lift_value,
        supportCount=row.support_count,
    )


@router.post("/run", response_model=AnalysisRunOut, status_code=status.HTTP_201_CREATED)
def run_analysis(payload: AnalysisRunCreate, db: Session = Depends(get_db)) -> AnalysisRun:
    run = AnalysisRun(
        run_name=payload.run_name,
        period_start=payload.period_start,
        period_end=payload.period_end,
        min_support=payload.min_support,
        min_confidence=payload.min_confidence,
        min_lift=payload.min_lift,
        status="processing",
    )
    db.add(run)
    db.flush()

    stmt = (
        select(LoanTransaction)
        .options(
            joinedload(LoanTransaction.student).joinedload(Student.department),
            joinedload(LoanTransaction.items).joinedload(LoanTransactionItem.book),
        )
        .order_by(LoanTransaction.id.asc())
    )
    if payload.period_start:
        stmt = stmt.where(LoanTransaction.loan_date >= payload.period_start)
    if payload.period_end:
        stmt = stmt.where(LoanTransaction.loan_date <= payload.period_end)

    transactions = db.execute(stmt).unique().scalars().all()
    baskets: list[list[str]] = []
    for txn in transactions:
        if not txn.student or not txn.student.department:
            continue
        items = [f"Jurusan:{txn.student.department.name}"]
        for item in txn.items:
            if item.book:
                items.append(f"Buku:{item.book.title}")
        baskets.append(items)

    frequent_itemsets, txn_count = generate_frequent_itemsets(
        baskets, min_support=payload.min_support
    )
    rules = generate_association_rules(
        frequent_itemsets=frequent_itemsets,
        transaction_count=txn_count,
        min_confidence=payload.min_confidence,
        min_lift=payload.min_lift,
    )

    for rule in rules:
        antecedent = list(rule.antecedent)
        consequent = list(rule.consequent)
        db.add(
            AssociationRule(
                analysis_run_id=run.id,
                antecedent_items=antecedent,
                consequent_items=consequent,
                antecedent_text=", ".join(antecedent),
                consequent_text=", ".join(consequent),
                support_value=rule.support,
                confidence_value=rule.confidence,
                lift_value=rule.lift,
                support_count=rule.support_count,
            )
        )

    run.status = "done"
    run.finished_at = datetime.utcnow()
    db.commit()
    db.refresh(run)
    return run


@router.get("/runs", response_model=list[AnalysisRunOut])
def list_runs(db: Session = Depends(get_db)) -> list[AnalysisRun]:
    return list(db.scalars(select(AnalysisRun).order_by(AnalysisRun.created_at.desc())))


@router.get("/runs/{run_id}", response_model=AnalysisRunOut)
def get_run(run_id: int, db: Session = Depends(get_db)) -> AnalysisRun:
    run = db.get(AnalysisRun, run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found.")
    return run


@router.delete("/runs/{run_id}", status_code=status.HTTP_200_OK)
def delete_run(run_id: int, db: Session = Depends(get_db)) -> dict[str, str]:
    run = db.get(AnalysisRun, run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found.")
    db.delete(run)
    db.commit()
    return {"message": f"Run {run_id} deleted."}


@router.get("/runs/{run_id}/rules", response_model=RulesResponse)
def get_rules(
    run_id: int,
    db: Session = Depends(get_db),
    department_id: int | None = None,
    q: str | None = None,
    min_confidence: float | None = Query(default=None, ge=0, le=1),
    min_lift: float | None = Query(default=None, ge=0),
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=100),
    sort_by: str = Query(default="lift"),
    sort_dir: str = Query(default="desc"),
) -> RulesResponse:
    run = db.get(AnalysisRun, run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found.")

    conditions = [AssociationRule.analysis_run_id == run_id]
    if q:
        pattern = f"%{q}%"
        conditions.append(
            or_(
                AssociationRule.antecedent_text.ilike(pattern),
                AssociationRule.consequent_text.ilike(pattern),
            )
        )
    if min_confidence is not None:
        conditions.append(AssociationRule.confidence_value >= min_confidence)
    if min_lift is not None:
        conditions.append(AssociationRule.lift_value >= min_lift)
    if department_id is not None:
        department = db.get(Department, department_id)
        if not department:
            raise HTTPException(status_code=404, detail="Department not found.")
        conditions.append(
            AssociationRule.antecedent_text.ilike(f"%Jurusan:{department.name}%")
        )

    sort_map = {
        "lift": AssociationRule.lift_value,
        "confidence": AssociationRule.confidence_value,
        "support": AssociationRule.support_value,
    }
    sort_col = sort_map.get(sort_by, AssociationRule.lift_value)
    order = sort_col.asc() if sort_dir == "asc" else sort_col.desc()

    count_stmt = select(func.count(AssociationRule.id)).where(and_(*conditions))
    total = int(db.scalar(count_stmt) or 0)
    total_pages = max(1, (total + limit - 1) // limit)

    stmt = (
        select(AssociationRule)
        .where(and_(*conditions))
        .order_by(order, AssociationRule.id.desc())
        .offset((page - 1) * limit)
        .limit(limit)
    )
    rows = list(db.scalars(stmt))

    top_rule_stmt = (
        select(AssociationRule)
        .where(AssociationRule.analysis_run_id == run_id)
        .order_by(AssociationRule.lift_value.desc(), AssociationRule.confidence_value.desc())
        .limit(1)
    )
    top_rule = db.scalar(top_rule_stmt)

    dominant_dept = None
    dept_counter: Counter[str] = Counter()
    all_run_rules = db.scalars(select(AssociationRule).where(AssociationRule.analysis_run_id == run_id)).all()
    for rr in all_run_rules:
        for item in rr.antecedent_items:
            if item.startswith("Jurusan:"):
                dept_counter[item.replace("Jurusan:", "").strip()] += 1
    if dept_counter:
        dominant_dept = dept_counter.most_common(1)[0][0]

    return RulesResponse(
        data=[_to_rule_out(row) for row in rows],
        meta=RulesMeta(page=page, limit=limit, total=total, totalPages=total_pages),
        summary=RulesSummary(
            totalRules=total,
            topLiftRule=_to_rule_out(top_rule) if top_rule else None,
            dominantDepartment=dominant_dept,
        ),
    )
