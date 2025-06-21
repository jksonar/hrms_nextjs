from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.schemas import EmployeeCreate, EmployeeUpdate, Employee
from app.services import crud
from app.core.security import get_current_active_user
from app.db.models import User as DBUser

router = APIRouter()

@router.post("/employees/", response_model=Employee, status_code=status.HTTP_201_CREATED)
def create_employee(employee: EmployeeCreate, db: Session = Depends(get_db), current_user: DBUser = Depends(get_current_active_user)):
    # Check if employee_id already exists
    db_employee = crud.get_employee_by_employee_id(db, employee_id=employee.employee_id)
    if db_employee:
        raise HTTPException(status_code=400, detail="Employee ID already registered")
    return crud.create_employee(db=db, employee=employee)

@router.get("/employees/", response_model=List[Employee])
def read_employees(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: DBUser = Depends(get_current_active_user)):
    employees = crud.get_employees(db, skip=skip, limit=limit)
    return employees

@router.get("/employees/{employee_id}", response_model=Employee)
def read_employee(employee_id: int, db: Session = Depends(get_db), current_user: DBUser = Depends(get_current_active_user)):
    db_employee = crud.get_employee(db, employee_id=employee_id)
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return db_employee

@router.put("/employees/{employee_id}", response_model=Employee)
def update_employee(employee_id: int, employee: EmployeeUpdate, db: Session = Depends(get_db), current_user: DBUser = Depends(get_current_active_user)):
    db_employee = crud.get_employee(db, employee_id=employee_id)
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return crud.update_employee(db=db, employee_id=employee_id, employee=employee)

@router.delete("/employees/{employee_id}")
def delete_employee(employee_id: int, db: Session = Depends(get_db), current_user: DBUser = Depends(get_current_active_user)):
    db_employee = crud.get_employee(db, employee_id=employee_id)
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    crud.delete_employee(db=db, employee_id=employee_id)
    return {"message": "Employee deleted successfully"}

@router.get("/employees/me/profile", response_model=Employee)
def read_my_profile(db: Session = Depends(get_db), current_user: DBUser = Depends(get_current_active_user)):
    db_employee = crud.get_employee_by_user_id(db, user_id=current_user.id)
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee profile not found")
    return db_employee