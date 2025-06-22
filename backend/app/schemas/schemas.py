from datetime import date, datetime
from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel, EmailStr

from app.db.models import AttendanceStatus, EmploymentStatus, LeaveStatus, UserRole

# User Schemas
class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str
    role: Optional[UserRole] = UserRole.EMPLOYEE


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None
    role: Optional[UserRole] = None


class User(UserBase):
    id: int
    is_active: bool
    role: UserRole

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Employee Schemas
class EmployeeBase(BaseModel):
    employee_id: str
    first_name: str
    last_name: str
    phone: Optional[str] = None
    address: Optional[str] = None
    date_of_birth: Optional[date] = None
    hire_date: Optional[date] = date.today()
    employment_status: Optional[EmploymentStatus] = EmploymentStatus.ACTIVE
    department_id: Optional[int] = None
    position_id: Optional[int] = None
    manager_id: Optional[int] = None
    salary: Optional[Decimal] = None


class EmployeeCreate(EmployeeBase):
    user_id: int


class EmployeeUpdate(EmployeeBase):
    employee_id: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    date_of_birth: Optional[date] = None
    hire_date: Optional[date] = None
    employment_status: Optional[EmploymentStatus] = None
    department_id: Optional[int] = None
    position_id: Optional[int] = None
    manager_id: Optional[int] = None
    salary: Optional[Decimal] = None


class Employee(EmployeeBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    department: Optional["Department"] = None
    position: Optional["Position"] = None
    manager: Optional["Employee"] = None
    subordinates: List["Employee"] = []
    attendance_records: List["Attendance"] = []
    leave_requests: List["LeaveRequest"] = []
    payroll_records: List["Payroll"] = []

    class Config:
        from_attributes = True

# Department Schemas
class DepartmentBase(BaseModel):
    name: str
    description: Optional[str] = None
    head_id: Optional[int] = None

class DepartmentCreate(DepartmentBase):
    pass

class DepartmentUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    head_id: Optional[int] = None

class Department(DepartmentBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Position Schemas
class PositionBase(BaseModel):
    title: str
    description: Optional[str] = None
    department_id: Optional[int] = None
    min_salary: Optional[Decimal] = None
    max_salary: Optional[Decimal] = None

class PositionCreate(PositionBase):
    pass

class PositionUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    department_id: Optional[int] = None
    min_salary: Optional[Decimal] = None
    max_salary: Optional[Decimal] = None

class Position(PositionBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Attendance Schemas
class AttendanceBase(BaseModel):
    employee_id: int
    date: date
    clock_in: Optional[datetime] = None
    clock_out: Optional[datetime] = None
    status: AttendanceStatus = AttendanceStatus.PRESENT
    notes: Optional[str] = None

class AttendanceCreate(AttendanceBase):
    pass

class AttendanceUpdate(BaseModel):
    clock_in: Optional[datetime] = None
    clock_out: Optional[datetime] = None
    status: Optional[AttendanceStatus] = None
    notes: Optional[str] = None

class Attendance(AttendanceBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Leave Request Schemas
class LeaveRequestBase(BaseModel):
    employee_id: int
    leave_type: str
    start_date: date
    end_date: date
    days_requested: int
    reason: Optional[str] = None

class LeaveRequestCreate(LeaveRequestBase):
    pass

class LeaveRequestUpdate(BaseModel):
    leave_type: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    days_requested: Optional[int] = None
    reason: Optional[str] = None
    status: Optional[LeaveStatus] = None

class LeaveRequest(LeaveRequestBase):
    id: int
    status: LeaveStatus
    approved_by: Optional[int] = None
    approved_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True

# Payroll Schemas
class PayrollBase(BaseModel):
    employee_id: int
    pay_period_start: date
    pay_period_end: date
    gross_salary: Decimal
    deductions: Decimal = Decimal('0')
    net_salary: Decimal
    tax_deduction: Decimal = Decimal('0')

class PayrollCreate(PayrollBase):
    pass

class PayrollUpdate(BaseModel):
    gross_salary: Optional[Decimal] = None
    deductions: Optional[Decimal] = None
    net_salary: Optional[Decimal] = None
    tax_deduction: Optional[Decimal] = None

class Payroll(PayrollBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True