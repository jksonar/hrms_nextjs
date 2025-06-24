from fastapi import APIRouter

from app.api.v1 import auth, users, employees, attendance, leave_requests, payroll, departments, positions, audit

api_router = APIRouter()
api_router.include_router(auth.router, tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(employees.router, prefix="/employees", tags=["employees"])
api_router.include_router(attendance.router, prefix="/attendance", tags=["attendance"])
api_router.include_router(leave_requests.router, prefix="/leave-requests", tags=["leave-requests"])
api_router.include_router(payroll.router, prefix="/payroll", tags=["payroll"])
api_router.include_router(departments.router, prefix="/departments", tags=["departments"])
api_router.include_router(positions.router, prefix="/positions", tags=["positions"])
api_router.include_router(audit.router, prefix="/audit", tags=["audit"])