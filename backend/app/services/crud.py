from sqlalchemy.orm import Session

from sqlalchemy.orm import Session
from datetime import date, datetime
from typing import Optional

from app.db.models import User, Employee, Department, Position, Attendance, LeaveRequest, Payroll, UserRole, EmploymentStatus, LeaveStatus, AttendanceStatus
from app.schemas.schemas import UserCreate, UserUpdate, EmployeeCreate, EmployeeUpdate, DepartmentCreate, DepartmentUpdate, PositionCreate, PositionUpdate, AttendanceCreate, AttendanceUpdate, LeaveRequestCreate, LeaveRequestUpdate, PayrollCreate, PayrollUpdate
from app.core.hashing import get_password_hash

# User CRUD Operations
def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()

def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = User(email=user.email, hashed_password=hashed_password, role=user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user: UserUpdate):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        update_data = user.dict(exclude_unset=True)
        if "password" in update_data:
            update_data["hashed_password"] = get_password_hash(update_data.pop("password"))
        for key, value in update_data.items():
            setattr(db_user, key, value)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user

# User Authentication
def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email=email)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

# Employee CRUD Operations
def get_employee(db: Session, employee_id: int):
    return db.query(Employee).filter(Employee.id == employee_id).first()

def get_employee_by_user_id(db: Session, user_id: int):
    return db.query(Employee).filter(Employee.user_id == user_id).first()

def get_employees(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Employee).offset(skip).limit(limit).all()

def create_employee(db: Session, employee: EmployeeCreate):
    db_employee = Employee(**employee.dict())
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee

def update_employee(db: Session, employee_id: int, employee: EmployeeUpdate):
    db_employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if db_employee:
        update_data = employee.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_employee, key, value)
        db.add(db_employee)
        db.commit()
        db.refresh(db_employee)
    return db_employee

def delete_employee(db: Session, employee_id: int):
    db_employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if db_employee:
        db.delete(db_employee)
        db.commit()
    return db_employee

# Department CRUD Operations
def get_department(db: Session, department_id: int):
    return db.query(Department).filter(Department.id == department_id).first()

def get_department_by_name(db: Session, name: str):
    return db.query(Department).filter(Department.name == name).first()

def get_departments(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Department).offset(skip).limit(limit).all()

def create_department(db: Session, department: DepartmentCreate):
    db_department = Department(**department.dict())
    db.add(db_department)
    db.commit()
    db.refresh(db_department)
    return db_department

def update_department(db: Session, department_id: int, department: DepartmentUpdate):
    db_department = db.query(Department).filter(Department.id == department_id).first()
    if db_department:
        update_data = department.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_department, key, value)
        db.add(db_department)
        db.commit()
        db.refresh(db_department)
    return db_department

def delete_department(db: Session, department_id: int):
    db_department = db.query(Department).filter(Department.id == department_id).first()
    if db_department:
        db.delete(db_department)
        db.commit()
    return db_department

def get_department_employees_count(db: Session, department_id: int):
    return db.query(Employee).filter(Employee.department_id == department_id).count()

# Position CRUD Operations
def get_position(db: Session, position_id: int):
    return db.query(Position).filter(Position.id == position_id).first()

def get_positions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Position).offset(skip).limit(limit).all()

def get_positions_by_department(db: Session, department_id: int):
    return db.query(Position).filter(Position.department_id == department_id).all()

def create_position(db: Session, position: PositionCreate):
    db_position = Position(**position.dict())
    db.add(db_position)
    db.commit()
    db.refresh(db_position)
    return db_position

def update_position(db: Session, position_id: int, position: PositionUpdate):
    db_position = db.query(Position).filter(Position.id == position_id).first()
    if db_position:
        update_data = position.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_position, key, value)
        db.add(db_position)
        db.commit()
        db.refresh(db_position)
    return db_position

def delete_position(db: Session, position_id: int):
    db_position = db.query(Position).filter(Position.id == position_id).first()
    if db_position:
        db.delete(db_position)
        db.commit()
    return db_position

def get_position_employees_count(db: Session, position_id: int):
    return db.query(Employee).filter(Employee.position_id == position_id).count()

# Attendance CRUD Operations
def get_attendance(db: Session, attendance_id: int):
    return db.query(Attendance).filter(Attendance.id == attendance_id).first()

def get_attendance_records(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Attendance).offset(skip).limit(limit).all()

def get_attendance_by_employee(db: Session, employee_id: int, skip: int = 0, limit: int = 100):
    return db.query(Attendance).filter(Attendance.employee_id == employee_id).offset(skip).limit(limit).all()

def create_attendance(db: Session, attendance: AttendanceCreate):
    db_attendance = Attendance(**attendance.dict())
    db.add(db_attendance)
    db.commit()
    db.refresh(db_attendance)
    return db_attendance

def update_attendance(db: Session, attendance_id: int, attendance: AttendanceUpdate):
    db_attendance = db.query(Attendance).filter(Attendance.id == attendance_id).first()
    if db_attendance:
        update_data = attendance.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_attendance, key, value)
        db.add(db_attendance)
        db.commit()
        db.refresh(db_attendance)
    return db_attendance

def clock_in(db: Session, employee_id: int):
    today = date.today()
    db_attendance = db.query(Attendance).filter(Attendance.employee_id == employee_id, Attendance.date == today).first()
    if db_attendance:
        return None # Already clocked in today
    
    new_attendance = Attendance(employee_id=employee_id, date=today, clock_in_time=datetime.now(), status=AttendanceStatus.present)
    db.add(new_attendance)
    db.commit()
    db.refresh(new_attendance)
    return new_attendance

def clock_out(db: Session, employee_id: int):
    today = date.today()
    db_attendance = db.query(Attendance).filter(Attendance.employee_id == employee_id, Attendance.date == today).first()
    if db_attendance and db_attendance.clock_in_time and not db_attendance.clock_out_time:
        db_attendance.clock_out_time = datetime.now()
        db.add(db_attendance)
        db.commit()
        db.refresh(db_attendance)
        return db_attendance
    return None # Not clocked in or already clocked out

# Leave Request CRUD Operations
def get_leave_request(db: Session, leave_id: int):
    return db.query(LeaveRequest).filter(LeaveRequest.id == leave_id).first()

def get_leave_requests(db: Session, skip: int = 0, limit: int = 100):
    return db.query(LeaveRequest).offset(skip).limit(limit).all()

def get_leave_requests_by_employee(db: Session, employee_id: int, skip: int = 0, limit: int = 100):
    return db.query(LeaveRequest).filter(LeaveRequest.employee_id == employee_id).offset(skip).limit(limit).all()

def get_pending_leave_requests_for_manager(db: Session, manager_id: int, skip: int = 0, limit: int = 100):
    # Assuming manager_id is linked to department or specific employees
    # This needs more complex logic based on how managers are linked to employees/departments
    # For now, a simplified version:
    return db.query(LeaveRequest).filter(LeaveRequest.status == LeaveStatus.pending).offset(skip).limit(limit).all()

def create_leave_request(db: Session, leave_request: LeaveRequestCreate):
    db_leave_request = LeaveRequest(**leave_request.dict())
    db.add(db_leave_request)
    db.commit()
    db.refresh(db_leave_request)
    return db_leave_request

def update_leave_request(db: Session, leave_id: int, leave_request: LeaveRequestUpdate):
    db_leave_request = db.query(LeaveRequest).filter(LeaveRequest.id == leave_id).first()
    if db_leave_request:
        update_data = leave_request.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_leave_request, key, value)
        db.add(db_leave_request)
        db.commit()
        db.refresh(db_leave_request)
    return db_leave_request

def approve_leave_request(db: Session, leave_id: int):
    db_leave_request = db.query(LeaveRequest).filter(LeaveRequest.id == leave_id).first()
    if db_leave_request:
        db_leave_request.status = LeaveStatus.approved
        db.add(db_leave_request)
        db.commit()
        db.refresh(db_leave_request)
    return db_leave_request

def reject_leave_request(db: Session, leave_id: int):
    db_leave_request = db.query(LeaveRequest).filter(LeaveRequest.id == leave_id).first()
    if db_leave_request:
        db_leave_request.status = LeaveStatus.rejected
        db.add(db_leave_request)
        db.commit()
        db.refresh(db_leave_request)
    return db_leave_request

# Payroll CRUD Operations
def get_payroll(db: Session, payroll_id: int):
    return db.query(Payroll).filter(Payroll.id == payroll_id).first()

def get_payroll_records(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Payroll).offset(skip).limit(limit).all()

def get_payroll_by_employee(db: Session, employee_id: int, skip: int = 0, limit: int = 100):
    return db.query(Payroll).filter(Payroll.employee_id == employee_id).offset(skip).limit(limit).all()

def create_payroll(db: Session, payroll: PayrollCreate):
    db_payroll = Payroll(**payroll.dict())
    db.add(db_payroll)
    db.commit()
    db.refresh(db_payroll)
    return db_payroll

def update_payroll(db: Session, payroll_id: int, payroll: PayrollUpdate):
    db_payroll = db.query(Payroll).filter(Payroll.id == payroll_id).first()
    if db_payroll:
        update_data = payroll.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_payroll, key, value)
        db.add(db_payroll)
        db.commit()
        db.refresh(db_payroll)
    return db_payroll

def delete_payroll(db: Session, payroll_id: int):
    db_payroll = db.query(Payroll).filter(Payroll.id == payroll_id).first()
    if db_payroll:
        db.delete(db_payroll)
        db.commit()
    return db_payroll

def generate_monthly_payroll(db: Session, month: int, year: int):
    # This is a simplified example. In a real HRMS, this would involve much more complex logic
    # including calculating gross pay, deductions, taxes, etc.
    employees = db.query(Employee).all()
    generated_payslips = []
    for employee in employees:
        # Check if payroll already exists for this employee for the given month/year
        existing_payroll = db.query(Payroll).filter(
            Payroll.employee_id == employee.id,
            Payroll.pay_date.like(f'{year}-{month:02d}-%') # Simple date matching
        ).first()

        if not existing_payroll:
            # Example: Basic salary calculation
            base_salary = employee.salary if employee.salary else 0
            net_pay = base_salary # Simplified

            payroll_data = PayrollCreate(
                employee_id=employee.id,
                pay_date=date(year, month, 25), # Assuming payday is 25th of the month
                gross_pay=base_salary,
                net_pay=net_pay,
                deductions=0.0,
                bonuses=0.0
            )
            db_payroll = Payroll(**payroll_data.dict())
            db.add(db_payroll)
            generated_payslips.append(db_payroll)
    
    db.commit()
    for payslip in generated_payslips:
        db.refresh(payslip)
    return generated_payslips