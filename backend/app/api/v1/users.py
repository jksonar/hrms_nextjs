from typing import List

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.schemas import UserCreate, UserUpdate, User
from app.services import crud
from app.core.security import get_current_active_user
from app.db.models import User as DBUser, UserRole
from app.core.security import role_required

router = APIRouter()

@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED, dependencies=[Depends(role_required([UserRole.ADMIN]))])
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@router.get("/me", response_model=User)
def read_users_me(current_user: DBUser = Depends(get_current_active_user)):
    return current_user

@router.get("/", response_model=List[User], dependencies=[Depends(role_required([UserRole.ADMIN]))])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: DBUser = Depends(get_current_active_user)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@router.get("/{user_id}", response_model=User, dependencies=[Depends(role_required([UserRole.ADMIN, UserRole.EMPLOYEE, UserRole.MANAGER, UserRole.HR]))])
def read_user(user_id: int, db: Session = Depends(get_db),
              current_user: DBUser = Depends(get_current_active_user)):
    if current_user.role != UserRole.ADMIN and current_user.id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to view this user's profile")
    user = crud.get_user(db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

@router.put("/{user_id}", response_model=User, dependencies=[Depends(role_required([UserRole.ADMIN]))])
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db), current_user: DBUser = Depends(get_current_active_user)):
    if current_user.role != UserRole.ADMIN and current_user.id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this user's profile")
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return crud.update_user(db=db, user_id=user_id, user=user)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(role_required([UserRole.ADMIN]))])
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    crud.delete_user(db=db, user_id=user_id)
    return {"message": "User deleted successfully"}