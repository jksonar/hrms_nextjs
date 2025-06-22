from typing import List
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.schemas import DepartmentCreate, DepartmentUpdate, Department
from app.services import crud
from app.core.security import get_current_active_user
from app.db.models import User as DBUser, UserRole
from app.core.security import role_required

router = APIRouter()

@router.post("/departments/", response_model=Department, status_code=status.HTTP_201_CREATED, dependencies=[Depends(role_required([UserRole.ADMIN, UserRole.HR]))])
def create_department(department: DepartmentCreate, db: Session = Depends(get_db)):
    # Check if department name already exists
    db_department = crud.get_department_by_name(db, name=department.name)
    if db_department:
        raise HTTPException(status_code=400, detail="Department name already exists")
    return crud.create_department(db=db, department=department)

@router.get("/departments/", response_model=List[Department], dependencies=[Depends(role_required([UserRole.ADMIN, UserRole.HR, UserRole.MANAGER, UserRole.EMPLOYEE]))])
def read_departments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    departments = crud.get_departments(db, skip=skip, limit=limit)
    return departments

@router.get("/departments/{department_id}", response_model=Department, dependencies=[Depends(role_required([UserRole.ADMIN, UserRole.HR, UserRole.MANAGER, UserRole.EMPLOYEE]))])
def read_department(department_id: int, db: Session = Depends(get_db)):
    db_department = crud.get_department(db, department_id=department_id)
    if db_department is None:
        raise HTTPException(status_code=404, detail="Department not found")
    return db_department

@router.put("/departments/{department_id}", response_model=Department, dependencies=[Depends(role_required([UserRole.ADMIN, UserRole.HR]))])
def update_department(department_id: int, department: DepartmentUpdate, db: Session = Depends(get_db)):
    db_department = crud.get_department(db, department_id=department_id)
    if db_department is None:
        raise HTTPException(status_code=404, detail="Department not found")
    
    # Check if new name already exists (if name is being updated)
    if department.name and department.name != db_department.name:
        existing_dept = crud.get_department_by_name(db, name=department.name)
        if existing_dept:
            raise HTTPException(status_code=400, detail="Department name already exists")
    
    return crud.update_department(db=db, department_id=department_id, department=department)

@router.delete("/departments/{department_id}", dependencies=[Depends(role_required([UserRole.ADMIN, UserRole.HR]))])
def delete_department(department_id: int, db: Session = Depends(get_db)):
    db_department = crud.get_department(db, department_id=department_id)
    if db_department is None:
        raise HTTPException(status_code=404, detail="Department not found")
    
    # Check if department has employees
    employees_count = crud.get_department_employees_count(db, department_id=department_id)
    if employees_count > 0:
        raise HTTPException(status_code=400, detail="Cannot delete department with existing employees")
    
    crud.delete_department(db=db, department_id=department_id)
    return {"message": "Department deleted successfully"}