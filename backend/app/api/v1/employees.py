from typing import List

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session

from app.core.security import get_current_active_user
from app.db.database import get_db
from app.db.models import Employee as DBEmployee, User as DBUser, UserRole
from app.schemas.schemas import Employee, EmployeeCreate, EmployeeUpdate
from app.services import crud
from app.services.rbac import can_access_employee
from app.services.audit import log_create, log_read, log_update, log_delete
from app.core.security import role_required

router = APIRouter()


@router.post("/", response_model=Employee, status_code=status.HTTP_201_CREATED, dependencies=[Depends(role_required([UserRole.ADMIN]))])
def create_employee(employee: EmployeeCreate, db: Session = Depends(get_db), current_user: DBUser = Depends(get_current_active_user), request: Request = None):
    db_employee = crud.get_employee_by_user_id(db, user_id=employee.user_id)
    if db_employee:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Employee with this user ID already exists")
    
    new_employee = crud.create_employee(db=db, employee=employee)
    
    # Log the creation
    log_create(db, current_user, "employees", new_employee.id, {
        "employee_id": new_employee.employee_id,
        "full_name": f"{new_employee.first_name} {new_employee.last_name}",
        "department_id": new_employee.department_id
    }, request)
    
    return new_employee


@router.get("/", response_model=List[Employee], dependencies=[Depends(role_required([UserRole.ADMIN, UserRole.HR, UserRole.MANAGER]))])
def read_employees(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: DBUser = Depends(get_current_active_user)):
    employees = crud.get_employees(db, skip=skip, limit=limit)
    return employees


@router.get("/me", response_model=Employee)
def read_current_employee(current_user: DBUser = Depends(get_current_active_user), db: Session = Depends(get_db)):
    employee = crud.get_employee_by_user_id(db, user_id=current_user.id)
    if not employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee profile not found")
    return employee


@router.get("/{employee_id}", response_model=Employee)
def read_employee(employee_id: int, db: Session = Depends(get_db), current_user: DBUser = Depends(get_current_active_user), request: Request = None):
    # Check RBAC permissions
    if not can_access_employee(current_user, employee_id, db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    
    employee = crud.get_employee(db, employee_id=employee_id)
    if employee is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
    
    # Log the read access
    log_read(db, current_user, "employees", employee_id, {
        "employee_id": employee.employee_id,
        "full_name": f"{employee.first_name} {employee.last_name}"
    }, request)
    
    return employee


@router.put("/{employee_id}", response_model=Employee, dependencies=[Depends(role_required([UserRole.ADMIN]))])
def update_employee(employee_id: int, employee: EmployeeUpdate, db: Session = Depends(get_db), current_user: DBUser = Depends(get_current_active_user), request: Request = None):
    db_employee = crud.get_employee(db, employee_id=employee_id)
    if db_employee is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
    
    # Store original data for audit log
    original_data = {
        "employee_id": db_employee.employee_id,
        "full_name": f"{db_employee.first_name} {db_employee.last_name}",
        "department_id": db_employee.department_id
    }
    
    updated_employee = crud.update_employee(db=db, employee_id=employee_id, employee=employee)
    
    # Log the update
    log_update(db, current_user, "employees", employee_id, {
        "employee_id": updated_employee.employee_id,
        "full_name": f"{updated_employee.first_name} {updated_employee.last_name}",
        "department_id": updated_employee.department_id,
        "original_data": original_data
    }, request)
    
    return updated_employee


@router.delete("/{employee_id}", response_model=dict)
def delete_employee(employee_id: int, db: Session = Depends(get_db), current_user: DBUser = Depends(role_required([UserRole.ADMIN])), request: Request = None):
    db_employee = crud.get_employee(db, employee_id=employee_id)
    if db_employee is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
    
    # Store data for audit log before deletion
    deleted_data = {
        "employee_id": db_employee.employee_id,
        "full_name": f"{db_employee.first_name} {db_employee.last_name}",
        "department_id": db_employee.department_id,
        "email": db_employee.user.email if db_employee.user else None
    }
    
    crud.delete_employee(db=db, employee_id=employee_id)
    
    # Log the deletion
    log_delete(db, current_user, "employees", employee_id, deleted_data, request)
    
    return {"message": "Employee deleted successfully"}