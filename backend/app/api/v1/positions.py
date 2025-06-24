from typing import List
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.schemas import PositionCreate, PositionUpdate, Position
from app.services import crud
from app.core.security import get_current_active_user
from app.db.models import User as DBUser, UserRole
from app.core.security import role_required

router = APIRouter()

@router.post("/", response_model=Position, status_code=status.HTTP_201_CREATED, dependencies=[Depends(role_required([UserRole.ADMIN]))])
def create_position(position: PositionCreate, db: Session = Depends(get_db)):
    return crud.create_position(db=db, position=position)

@router.get("/", response_model=List[Position], dependencies=[Depends(role_required([UserRole.ADMIN, UserRole.HR, UserRole.MANAGER, UserRole.EMPLOYEE]))])
def read_positions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    positions = crud.get_positions(db, skip=skip, limit=limit)
    return positions

@router.get("/department/{department_id}", response_model=List[Position], dependencies=[Depends(role_required([UserRole.ADMIN, UserRole.HR, UserRole.MANAGER, UserRole.EMPLOYEE]))])
def read_positions_by_department(department_id: int, db: Session = Depends(get_db)):
    positions = crud.get_positions_by_department(db, department_id=department_id)
    return positions

@router.get("/{position_id}", response_model=Position, dependencies=[Depends(role_required([UserRole.ADMIN, UserRole.HR, UserRole.MANAGER, UserRole.EMPLOYEE]))])
def read_position(position_id: int, db: Session = Depends(get_db)):
    db_position = crud.get_position(db, position_id=position_id)
    if db_position is None:
        raise HTTPException(status_code=404, detail="Position not found")
    return db_position

@router.put("/{position_id}", response_model=Position, dependencies=[Depends(role_required([UserRole.ADMIN]))])
def update_position(position_id: int, position: PositionUpdate, db: Session = Depends(get_db)):
    db_position = crud.get_position(db, position_id=position_id)
    if db_position is None:
        raise HTTPException(status_code=404, detail="Position not found")
    return crud.update_position(db=db, position_id=position_id, position=position)

@router.delete("/{position_id}", dependencies=[Depends(role_required([UserRole.ADMIN]))])
def delete_position(position_id: int, db: Session = Depends(get_db)):
    db_position = crud.get_position(db, position_id=position_id)
    if db_position is None:
        raise HTTPException(status_code=404, detail="Position not found")
    
    # Check if position has employees
    employees_count = crud.get_position_employees_count(db, position_id=position_id)
    if employees_count > 0:
        raise HTTPException(status_code=400, detail="Cannot delete position with existing employees")
    
    crud.delete_position(db=db, position_id=position_id)
    return {"message": "Position deleted successfully"}