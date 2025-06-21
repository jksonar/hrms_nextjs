from datetime import date, datetime
import enum
from datetime import date
from sqlalchemy import Boolean, Column, Date, DateTime, Enum, ForeignKey, Integer, Numeric, String, Text

from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.database import Base

# Enums
class UserRole(enum.Enum):
    EMPLOYEE = "employee"
    MANAGER = "manager"
    HR = "hr"
    ADMIN = "admin"

class EmploymentStatus(enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    TERMINATED = "terminated"
    ON_LEAVE = "on_leave"

class LeaveStatus(enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    CANCELLED = "cancelled"

class AttendanceStatus(enum.Enum):
    PRESENT = "present"
    ABSENT = "absent"
    LATE = "late"
    HALF_DAY = "half_day"

# Models
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    role = Column(Enum(UserRole), default=UserRole.EMPLOYEE, nullable=False)

    employee = relationship("Employee", back_populates="user", uselist=False)


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    employee_id = Column(String, unique=True, index=True, nullable=False)
    first_name = Column(String, index=True, nullable=False)
    last_name = Column(String, index=True, nullable=False)
    phone = Column(String)
    address = Column(Text)
    date_of_birth = Column(Date)
    hire_date = Column(Date, default=date.today)
    employment_status = Column(Enum(EmploymentStatus), default=EmploymentStatus.ACTIVE)
    department_id = Column(Integer, ForeignKey("departments.id"))
    position_id = Column(Integer, ForeignKey("positions.id"))
    manager_id = Column(Integer, ForeignKey("employees.id"))
    salary = Column(Numeric(10, 2))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="employee")
    department = relationship("Department", back_populates="employees", foreign_keys=[department_id])
    position = relationship("Position", back_populates="employees")
    manager = relationship("Employee", remote_side=[id], back_populates="subordinates", foreign_keys=[manager_id])
    subordinates = relationship("Employee", back_populates="manager", foreign_keys=[manager_id])
    attendance_records = relationship("Attendance", back_populates="employee")
    leave_requests = relationship("LeaveRequest", back_populates="employee", foreign_keys="LeaveRequest.employee_id")
    payroll_records = relationship("Payroll", back_populates="employee")

class Department(Base):
    __tablename__ = "departments"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(Text)
    head_id = Column(Integer, ForeignKey("employees.id"))
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    employees = relationship("Employee", back_populates="department", foreign_keys="Employee.department_id")
    head = relationship("Employee", foreign_keys=[head_id])

class Position(Base):
    __tablename__ = "positions"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    department_id = Column(Integer, ForeignKey("departments.id"))
    min_salary = Column(Numeric(10, 2))
    max_salary = Column(Numeric(10, 2))
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    employees = relationship("Employee", back_populates="position")

class Attendance(Base):
    __tablename__ = "attendance"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    date = Column(Date, index=True)
    clock_in = Column(DateTime)
    clock_out = Column(DateTime)
    status = Column(Enum(AttendanceStatus), default=AttendanceStatus.PRESENT)
    notes = Column(Text)
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    employee = relationship("Employee", back_populates="attendance_records")

class LeaveRequest(Base):
    __tablename__ = "leave_requests"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    leave_type = Column(String)  # sick, vacation, personal, etc.
    start_date = Column(Date)
    end_date = Column(Date)
    days_requested = Column(Integer)
    reason = Column(Text)
    status = Column(Enum(LeaveStatus), default=LeaveStatus.PENDING)
    approved_by = Column(Integer, ForeignKey("employees.id"))
    approved_at = Column(DateTime)
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    employee = relationship("Employee", back_populates="leave_requests", foreign_keys=[employee_id])
    approver = relationship("Employee", foreign_keys=[approved_by])

class Payroll(Base):
    __tablename__ = "payroll"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    pay_period_start = Column(Date)
    pay_period_end = Column(Date)
    gross_salary = Column(Numeric(10, 2))
    deductions = Column(Numeric(10, 2), default=0)
    net_salary = Column(Numeric(10, 2))
    tax_deduction = Column(Numeric(10, 2), default=0)
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    employee = relationship("Employee", back_populates="payroll_records")