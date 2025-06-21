from fastapi import APIRouter

from app.api.v1 import auth, users, employees, attendance, leave_requests, payroll, departments, positions

api_router = APIRouter()
api_router.include_router(auth.router, tags=["auth"])
api_router.include_router(users.router, tags=["users"])
api_router.include_router(employees.router, tags=["employees"])
api_router.include_router(attendance.router, tags=["attendance"])
api_router.include_router(leave_requests.router, tags=["leave-requests"])
api_router.include_router(payroll.router, tags=["payroll"])
api_router.include_router(departments.router, tags=["departments"])
api_router.include_router(positions.router, tags=["positions"])