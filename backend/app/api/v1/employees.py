from typing import List

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import get_current_active_user
from app.db.database import get_db
from app.db.models import Employee as DBEmployee, User as DBUser, UserRole
from app.schemas.schemas import Employee, EmployeeCreate, EmployeeUpdate
from app.services import crud
from app.core.security import role_required

router = APIRouter()


@router.post("/", response_model=Employee, status_code=status.HTTP_201_CREATED, dependencies=[Depends(role_required([UserRole.ADMIN]))])
def create_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
    db_employee = crud.get_employee_by_user_id(db, user_id=employee.user_id)
    if db_employee:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Employee with this user ID already exists")
    return crud.create_employee(db=db, employee=employee)


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
def read_employee(employee_id: int, db: Session = Depends(get_db), current_user: DBUser = Depends(get_current_active_user)):
    if current_user.role not in [UserRole.ADMIN, UserRole.HR, UserRole.MANAGER] and \
       (current_user.role == UserRole.EMPLOYEE and crud.get_employee_by_user_id(db, user_id=current_user.id).id != employee_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    employee = crud.get_employee(db, employee_id=employee_id)
    if employee is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
    return employee


@router.put("/{employee_id}", response_model=Employee, dependencies=[Depends(role_required([UserRole.ADMIN]))])
def update_employee(employee_id: int, employee: EmployeeUpdate, db: Session = Depends(get_db), current_user: DBUser = Depends(get_current_active_user)): 
    db_employee = crud.get_employee(db, employee_id=employee_id)
    if db_employee is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
    return crud.update_employee(db=db, employee_id=employee_id, employee=employee)


@router.delete("/{employee_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(role_required([UserRole.ADMIN]))])
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    employee = crud.get_employee(db, employee_id=employee_id)
    if employee is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
    crud.delete_employee(db, employee_id=employee_id)
    return {"ok": True}