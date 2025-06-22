from typing import List
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.schemas import LeaveRequestCreate, LeaveRequestUpdate, LeaveRequest
from app.services import crud
from app.core.security import get_current_active_user
from app.db.models import User as DBUser, LeaveStatus, UserRole
from app.core.security import role_required

router = APIRouter()

@router.post("/leave-requests/", response_model=LeaveRequest, status_code=status.HTTP_201_CREATED, dependencies=[Depends(role_required([UserRole.EMPLOYEE]))])
def create_leave_request(leave_request: LeaveRequestCreate, db: Session = Depends(get_db), current_user: DBUser = Depends(get_current_active_user)):
    return crud.create_leave_request(db=db, leave_request=leave_request)

@router.get("/leave-requests/", response_model=List[LeaveRequest], dependencies=[Depends(role_required([UserRole.ADMIN, UserRole.HR, UserRole.MANAGER]))])
def read_leave_requests(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    leave_requests = crud.get_leave_requests(db, skip=skip, limit=limit)
    return leave_requests

@router.get("/leave-requests/employee/{employee_id}", response_model=List[LeaveRequest], dependencies=[Depends(role_required([UserRole.ADMIN, UserRole.HR, UserRole.MANAGER]))])
def read_employee_leave_requests(employee_id: int, db: Session = Depends(get_db)):
    leave_requests = crud.get_employee_leave_requests(db, employee_id=employee_id)
    return leave_requests

@router.get("/leave-requests/{leave_request_id}", response_model=LeaveRequest, dependencies=[Depends(role_required([UserRole.ADMIN, UserRole.HR, UserRole.MANAGER, UserRole.EMPLOYEE]))])
def read_leave_request(leave_request_id: int, db: Session = Depends(get_db)):
    db_leave_request = crud.get_leave_request(db, leave_request_id=leave_request_id)
    if db_leave_request is None:
        raise HTTPException(status_code=404, detail="Leave request not found")
    return db_leave_request

@router.put("/leave-requests/{leave_request_id}", response_model=LeaveRequest, dependencies=[Depends(role_required([UserRole.ADMIN, UserRole.HR, UserRole.MANAGER]))])
def update_leave_request(leave_request_id: int, leave_request: LeaveRequestUpdate, db: Session = Depends(get_db)):
    db_leave_request = crud.get_leave_request(db, leave_request_id=leave_request_id)
    if db_leave_request is None:
        raise HTTPException(status_code=404, detail="Leave request not found")
    return crud.update_leave_request(db=db, leave_request_id=leave_request_id, leave_request=leave_request)

@router.post("/leave-requests/{leave_request_id}/approve", dependencies=[Depends(role_required([UserRole.ADMIN, UserRole.HR, UserRole.MANAGER]))])
def approve_leave_request(leave_request_id: int, db: Session = Depends(get_db), current_user: DBUser = Depends(get_current_active_user)):
    db_leave_request = crud.get_leave_request(db, leave_request_id=leave_request_id)
    if db_leave_request is None:
        raise HTTPException(status_code=404, detail="Leave request not found")
    
    # Get current user's employee record to use as approver
    approver_employee = crud.get_employee_by_user_id(db, user_id=current_user.id)
    if not approver_employee:
        raise HTTPException(status_code=404, detail="Approver employee profile not found")
    
    leave_request_update = LeaveRequestUpdate(status=LeaveStatus.APPROVED)
    updated_request = crud.update_leave_request(db=db, leave_request_id=leave_request_id, leave_request=leave_request_update)
    
    # Set approver information
    crud.set_leave_request_approver(db=db, leave_request_id=leave_request_id, approver_id=approver_employee.id)
    
    return {"message": "Leave request approved successfully"}

@router.post("/leave-requests/{leave_request_id}/reject", dependencies=[Depends(role_required([UserRole.ADMIN, UserRole.HR, UserRole.MANAGER]))])
def reject_leave_request(leave_request_id: int, db: Session = Depends(get_db), current_user: DBUser = Depends(get_current_active_user)):
    db_leave_request = crud.get_leave_request(db, leave_request_id=leave_request_id)
    if db_leave_request is None:
        raise HTTPException(status_code=404, detail="Leave request not found")
    
    # Get current user's employee record to use as approver
    approver_employee = crud.get_employee_by_user_id(db, user_id=current_user.id)
    if not approver_employee:
        raise HTTPException(status_code=404, detail="Approver employee profile not found")
    
    leave_request_update = LeaveRequestUpdate(status=LeaveStatus.REJECTED)
    updated_request = crud.update_leave_request(db=db, leave_request_id=leave_request_id, leave_request=leave_request_update)
    
    # Set approver information
    crud.set_leave_request_approver(db=db, leave_request_id=leave_request_id, approver_id=approver_employee.id)
    
    return {"message": "Leave request rejected"}

@router.get("/leave-requests/my-requests", response_model=List[LeaveRequest], dependencies=[Depends(role_required([UserRole.EMPLOYEE]))])
def read_my_leave_requests(db: Session = Depends(get_db), current_user: DBUser = Depends(get_current_active_user)):
    # Get current user's employee record
    employee = crud.get_employee_by_user_id(db, user_id=current_user.id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee profile not found")
    
    leave_requests = crud.get_employee_leave_requests(db, employee_id=employee.id)
    return leave_requests

@router.get("/leave-requests/pending-approvals", response_model=List[LeaveRequest], dependencies=[Depends(role_required([UserRole.MANAGER]))])
def read_pending_leave_requests(db: Session = Depends(get_db), current_user: DBUser = Depends(get_current_active_user)):
    # Get current user's employee record
    manager_employee = crud.get_employee_by_user_id(db, user_id=current_user.id)
    if not manager_employee:
        raise HTTPException(status_code=404, detail="Manager employee profile not found")
    
    # Get pending leave requests for employees under this manager
    pending_requests = crud.get_pending_leave_requests_for_manager(db, manager_id=manager_employee.id)
    return pending_requests