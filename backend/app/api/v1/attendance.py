from typing import List
from datetime import date, datetime
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.schemas import AttendanceCreate, AttendanceUpdate, Attendance
from app.services import crud
from app.core.security import get_current_active_user
from app.db.models import User as DBUser, UserRole
from app.core.security import role_required

router = APIRouter()

@router.post("/attendance/", response_model=Attendance, status_code=status.HTTP_201_CREATED, dependencies=[Depends(role_required([UserRole.ADMIN, UserRole.HR]))])
def create_attendance(attendance: AttendanceCreate, db: Session = Depends(get_db)):
    # Check if attendance already exists for this employee and date
    existing_attendance = crud.get_attendance_by_employee_and_date(db, employee_id=attendance.employee_id, date=attendance.date)
    if existing_attendance:
        raise HTTPException(status_code=400, detail="Attendance already recorded for this date")
    return crud.create_attendance(db=db, attendance=attendance)

@router.get("/attendance/", response_model=List[Attendance], dependencies=[Depends(role_required([UserRole.ADMIN, UserRole.HR, UserRole.MANAGER]))])
def read_attendance(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    attendance_records = crud.get_attendance_records(db, skip=skip, limit=limit)
    return attendance_records

@router.get("/attendance/employee/{employee_id}", response_model=List[Attendance], dependencies=[Depends(role_required([UserRole.ADMIN, UserRole.HR, UserRole.MANAGER]))])
def read_employee_attendance(employee_id: int, start_date: date = None, end_date: date = None, db: Session = Depends(get_db)):
    attendance_records = crud.get_employee_attendance(db, employee_id=employee_id, start_date=start_date, end_date=end_date)
    return attendance_records

@router.get("/attendance/{attendance_id}", response_model=Attendance, dependencies=[Depends(role_required([UserRole.ADMIN, UserRole.HR, UserRole.MANAGER, UserRole.EMPLOYEE]))])
def read_attendance_record(attendance_id: int, db: Session = Depends(get_db)):
    db_attendance = crud.get_attendance(db, attendance_id=attendance_id)
    if db_attendance is None:
        raise HTTPException(status_code=404, detail="Attendance record not found")
    return db_attendance

@router.put("/attendance/{attendance_id}", response_model=Attendance, dependencies=[Depends(role_required([UserRole.ADMIN, UserRole.HR, UserRole.MANAGER]))])
def update_attendance(attendance_id: int, attendance: AttendanceUpdate, db: Session = Depends(get_db)):
    db_attendance = crud.get_attendance(db, attendance_id=attendance_id)
    if db_attendance is None:
        raise HTTPException(status_code=404, detail="Attendance record not found")
    return crud.update_attendance(db=db, attendance_id=attendance_id, attendance=attendance)

@router.post("/attendance/clock-in", dependencies=[Depends(role_required([UserRole.EMPLOYEE]))])
def clock_in(employee_id: int, db: Session = Depends(get_db)):
    today = date.today()
    existing_attendance = crud.get_attendance_by_employee_and_date(db, employee_id=employee_id, date=today)
    
    if existing_attendance and existing_attendance.clock_in:
        raise HTTPException(status_code=400, detail="Already clocked in for today")
    
    if existing_attendance:
        # Update existing record
        attendance_update = AttendanceUpdate(clock_in=datetime.now())
        return crud.update_attendance(db=db, attendance_id=existing_attendance.id, attendance=attendance_update)
    else:
        # Create new record
        attendance_create = AttendanceCreate(employee_id=employee_id, date=today, clock_in=datetime.now())
        return crud.create_attendance(db=db, attendance=attendance_create)

@router.post("/attendance/clock-out", dependencies=[Depends(role_required([UserRole.EMPLOYEE]))])
def clock_out(employee_id: int, db: Session = Depends(get_db)):
    today = date.today()
    existing_attendance = crud.get_attendance_by_employee_and_date(db, employee_id=employee_id, date=today)
    
    if not existing_attendance or not existing_attendance.clock_in:
        raise HTTPException(status_code=400, detail="Must clock in first")
    
    if existing_attendance.clock_out:
        raise HTTPException(status_code=400, detail="Already clocked out for today")
    
    attendance_update = AttendanceUpdate(clock_out=datetime.now())
    return crud.update_attendance(db=db, attendance_id=existing_attendance.id, attendance=attendance_update)

@router.get("/attendance/my-records", response_model=List[Attendance], dependencies=[Depends(role_required([UserRole.EMPLOYEE]))])
def read_my_attendance(start_date: date = None, end_date: date = None, db: Session = Depends(get_db)):
    # Get current user's employee record
    employee = crud.get_employee_by_user_id(db, user_id=current_user.id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee profile not found")
    
    attendance_records = crud.get_employee_attendance(db, employee_id=employee.id, start_date=start_date, end_date=end_date)
    return attendance_records