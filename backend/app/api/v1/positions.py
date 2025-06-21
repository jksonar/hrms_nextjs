from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.schemas import PositionCreate, PositionUpdate, Position
from app.services import crud
from app.core.security import get_current_active_user
from app.db.models import User as DBUser

router = APIRouter()

@router.post("/positions/", response_model=Position, status_code=status.HTTP_201_CREATED)
def create_position(position: PositionCreate, db: Session = Depends(get_db), current_user: DBUser = Depends(get_current_active_user)):
    return crud.create_position(db=db, position=position)

@router.get("/positions/", response_model=List[Position])
def read_positions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: DBUser = Depends(get_current_active_user)):
    positions = crud.get_positions(db, skip=skip, limit=limit)
    return positions

@router.get("/positions/department/{department_id}", response_model=List[Position])
def read_positions_by_department(department_id: int, db: Session = Depends(get_db), current_user: DBUser = Depends(get_current_active_user)):
    positions = crud.get_positions_by_department(db, department_id=department_id)
    return positions

@router.get("/positions/{position_id}", response_model=Position)
def read_position(position_id: int, db: Session = Depends(get_db), current_user: DBUser = Depends(get_current_active_user)):
    db_position = crud.get_position(db, position_id=position_id)
    if db_position is None:
        raise HTTPException(status_code=404, detail="Position not found")
    return db_position

@router.put("/positions/{position_id}", response_model=Position)
def update_position(position_id: int, position: PositionUpdate, db: Session = Depends(get_db), current_user: DBUser = Depends(get_current_active_user)):
    db_position = crud.get_position(db, position_id=position_id)
    if db_position is None:
        raise HTTPException(status_code=404, detail="Position not found")
    return crud.update_position(db=db, position_id=position_id, position=position)

@router.delete("/positions/{position_id}")
def delete_position(position_id: int, db: Session = Depends(get_db), current_user: DBUser = Depends(get_current_active_user)):
    db_position = crud.get_position(db, position_id=position_id)
    if db_position is None:
        raise HTTPException(status_code=404, detail="Position not found")
    
    # Check if position has employees
    employees_count = crud.get_position_employees_count(db, position_id=position_id)
    if employees_count > 0:
        raise HTTPException(status_code=400, detail="Cannot delete position with existing employees")
    
    crud.delete_position(db=db, position_id=position_id)
    return {"message": "Position deleted successfully"}