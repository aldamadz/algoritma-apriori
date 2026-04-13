from fastapi import APIRouter

from app.api.routes import analysis, books, departments, health, students, transactions

api_router = APIRouter(prefix="/api")
api_router.include_router(health.router, tags=["health"])
api_router.include_router(departments.router, prefix="/departments", tags=["departments"])
api_router.include_router(students.router, prefix="/students", tags=["students"])
api_router.include_router(books.router, prefix="/books", tags=["books"])
api_router.include_router(transactions.router, prefix="/transactions", tags=["transactions"])
api_router.include_router(analysis.router, prefix="/analysis", tags=["analysis"])
