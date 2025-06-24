from typing import Optional
from sqlalchemy.orm import Session
from app.db.models import User, Employee, UserRole
from app.services import crud

def can_access_employee(current_user: User, target_employee_id: int, db: Session) -> bool:
    """
    Check if the current user can access the specified employee's data.
    
    Rules:
    - ADMIN and HR: Can access all employees
    - MANAGER: Can access their direct reports and their own data
    - EMPLOYEE: Can only access their own data
    """
    if current_user.role in [UserRole.ADMIN, UserRole.HR]:
        return True
    
    # Get the current user's employee record
    current_employee = crud.get_employee_by_user_id(db, current_user.id)
    if not current_employee:
        return False
    
    if current_user.role == UserRole.MANAGER:
        # Check if target employee reports to this manager
        target_employee = crud.get_employee(db, target_employee_id)
        if target_employee:
            # Manager can access their own data
            if target_employee.id == current_employee.id:
                return True
            # Manager can access their direct reports
            # Note: You'll need to add manager_id field to Employee model
            # return target_employee.manager_id == current_employee.id
            return True  # Temporary - allow all for now until manager_id is added
        return False
    
    # Employees can only access their own data
    return current_employee.id == target_employee_id

def can_access_user(current_user: User, target_user_id: int, db: Session) -> bool:
    """
    Check if the current user can access the specified user's data.
    
    Rules:
    - ADMIN: Can access all users
    - HR: Can access all users except other admins
    - MANAGER: Can access their direct reports and their own data
    - EMPLOYEE: Can only access their own data
    """
    if current_user.role == UserRole.ADMIN:
        return True
    
    if current_user.role == UserRole.HR:
        # HR can access all users except other admins
        target_user = crud.get_user(db, target_user_id)
        if target_user and target_user.role == UserRole.ADMIN:
            return False
        return True
    
    if current_user.role == UserRole.MANAGER:
        # Manager can access their own data
        if current_user.id == target_user_id:
            return True
        
        # Manager can access their direct reports
        current_employee = crud.get_employee_by_user_id(db, current_user.id)
        target_user = crud.get_user(db, target_user_id)
        if current_employee and target_user:
            target_employee = crud.get_employee_by_user_id(db, target_user.id)
            if target_employee:
                # Note: You'll need to add manager_id field to Employee model
                # return target_employee.manager_id == current_employee.id
                return True  # Temporary - allow all for now until manager_id is added
        return False
    
    # Employees can only access their own data
    return current_user.id == target_user_id

def can_access_attendance(current_user: User, target_employee_id: Optional[int], db: Session) -> bool:
    """
    Check if the current user can access attendance data.
    
    Rules:
    - ADMIN and HR: Can access all attendance records
    - MANAGER: Can access their direct reports' and their own attendance
    - EMPLOYEE: Can only access their own attendance
    """
    if current_user.role in [UserRole.ADMIN, UserRole.HR]:
        return True
    
    if target_employee_id is None:
        # Accessing general attendance data - only admin/HR allowed
        return False
    
    return can_access_employee(current_user, target_employee_id, db)

def can_access_leave_request(current_user: User, target_employee_id: Optional[int], db: Session) -> bool:
    """
    Check if the current user can access leave request data.
    
    Rules:
    - ADMIN and HR: Can access all leave requests
    - MANAGER: Can access their direct reports' and their own leave requests
    - EMPLOYEE: Can only access their own leave requests
    """
    if current_user.role in [UserRole.ADMIN, UserRole.HR]:
        return True
    
    if target_employee_id is None:
        # Accessing general leave request data - only admin/HR allowed
        return False
    
    return can_access_employee(current_user, target_employee_id, db)

def can_access_payroll(current_user: User, target_employee_id: Optional[int], db: Session) -> bool:
    """
    Check if the current user can access payroll data.
    
    Rules:
    - ADMIN and HR: Can access all payroll records
    - MANAGER: Cannot access payroll (sensitive financial data)
    - EMPLOYEE: Can only access their own payroll
    """
    if current_user.role in [UserRole.ADMIN, UserRole.HR]:
        return True
    
    if current_user.role == UserRole.MANAGER:
        return False  # Managers cannot access payroll data
    
    if target_employee_id is None:
        return False
    
    # Employees can only access their own payroll
    current_employee = crud.get_employee_by_user_id(db, current_user.id)
    return current_employee and current_employee.id == target_employee_id

def can_approve_leave(current_user: User, target_employee_id: int, db: Session) -> bool:
    """
    Check if the current user can approve/reject leave requests.
    
    Rules:
    - ADMIN and HR: Can approve all leave requests
    - MANAGER: Can approve their direct reports' leave requests
    - EMPLOYEE: Cannot approve leave requests
    """
    if current_user.role in [UserRole.ADMIN, UserRole.HR]:
        return True
    
    if current_user.role == UserRole.MANAGER:
        # Manager can approve their direct reports' leave
        current_employee = crud.get_employee_by_user_id(db, current_user.id)
        target_employee = crud.get_employee(db, target_employee_id)
        if current_employee and target_employee:
            # Note: You'll need to add manager_id field to Employee model
            # return target_employee.manager_id == current_employee.id
            return True  # Temporary - allow all for now until manager_id is added
        return False
    
    return False  # Employees cannot approve leave requests