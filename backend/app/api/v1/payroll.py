from typing import List
from datetime import date
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.schemas import PayrollCreate, PayrollUpdate, Payroll
from app.services import crud
from app.core.security import get_current_active_user
from app.db.models import User as DBUser, UserRole
from app.core.security import role_required

router = APIRouter()

@router.post("/", response_model=Payroll, status_code=status.HTTP_201_CREATED, dependencies=[Depends(role_required([UserRole.ADMIN, UserRole.HR]))])
def create_payroll(payroll: PayrollCreate, db: Session = Depends(get_db)):
    # Check if payroll already exists for this employee and period
    existing_payroll = crud.get_payroll_by_employee_and_period(db, employee_id=payroll.employee_id, start_date=payroll.pay_period_start, end_date=payroll.pay_period_end)
    if existing_payroll:
        raise HTTPException(status_code=400, detail="Payroll already exists for this period")
    return crud.create_payroll(db=db, payroll=payroll)

@router.get("/", response_model=List[Payroll], dependencies=[Depends(role_required([UserRole.ADMIN, UserRole.HR, UserRole.MANAGER]))])
def read_payroll_records(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    payroll_records = crud.get_payroll_records(db, skip=skip, limit=limit)
    return payroll_records

@router.get("/employee/{employee_id}", response_model=List[Payroll], dependencies=[Depends(role_required([UserRole.ADMIN, UserRole.HR, UserRole.MANAGER]))])
def read_employee_payroll(employee_id: int, year: int = None, db: Session = Depends(get_db)):
    payroll_records = crud.get_employee_payroll(db, employee_id=employee_id, year=year)
    return payroll_records

@router.get("/{payroll_id}", response_model=Payroll, dependencies=[Depends(role_required([UserRole.ADMIN, UserRole.HR, UserRole.MANAGER, UserRole.EMPLOYEE]))])
def read_payroll_record(payroll_id: int, db: Session = Depends(get_db)):
    db_payroll = crud.get_payroll(db, payroll_id=payroll_id)
    if db_payroll is None:
        raise HTTPException(status_code=404, detail="Payroll record not found")
    return db_payroll

@router.put("/{payroll_id}", response_model=Payroll, dependencies=[Depends(role_required([UserRole.ADMIN, UserRole.HR]))])
def update_payroll(payroll_id: int, payroll: PayrollUpdate, db: Session = Depends(get_db)):
    db_payroll = crud.get_payroll(db, payroll_id=payroll_id)
    if db_payroll is None:
        raise HTTPException(status_code=404, detail="Payroll record not found")
    return crud.update_payroll(db=db, payroll_id=payroll_id, payroll=payroll)

@router.delete("/{payroll_id}", dependencies=[Depends(role_required([UserRole.ADMIN, UserRole.HR]))])
def delete_payroll(payroll_id: int, db: Session = Depends(get_db)):
    db_payroll = crud.get_payroll(db, payroll_id=payroll_id)
    if db_payroll is None:
        raise HTTPException(status_code=404, detail="Payroll record not found")
    crud.delete_payroll(db=db, payroll_id=payroll_id)
    return {"message": "Payroll record deleted successfully"}

@router.get("/payroll/my-payslips", response_model=List[Payroll], dependencies=[Depends(role_required([UserRole.EMPLOYEE]))])
def read_my_payslips(year: int = None, db: Session = Depends(get_db), current_user: DBUser = Depends(get_current_active_user)):
    # Get current user's employee record
    employee = crud.get_employee_by_user_id(db, user_id=current_user.id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee profile not found")
    
    payroll_records = crud.get_employee_payroll(db, employee_id=employee.id, year=year)
    return payroll_records

@router.post("/payroll/generate-monthly", dependencies=[Depends(role_required([UserRole.ADMIN, UserRole.HR]))])
def generate_monthly_payroll(year: int, month: int, db: Session = Depends(get_db)):
    """Generate payroll for all active employees for a specific month"""
    try:
        # Get all active employees
        employees = crud.get_active_employees(db)
        
        # Calculate pay period dates
        from calendar import monthrange
        _, last_day = monthrange(year, month)
        pay_period_start = date(year, month, 1)
        pay_period_end = date(year, month, last_day)
        
        generated_count = 0
        for employee in employees:
            # Check if payroll already exists
            existing_payroll = crud.get_payroll_by_employee_and_period(
                db, 
                employee_id=employee.id, 
                start_date=pay_period_start, 
                end_date=pay_period_end
            )
            
            if not existing_payroll:
                # Calculate net salary (basic calculation)
                gross_salary = employee.salary or 0
                tax_deduction = gross_salary * 0.1  # 10% tax (simplified)
                other_deductions = 0  # Can be expanded
                net_salary = gross_salary - tax_deduction - other_deductions
                
                payroll_data = PayrollCreate(
                    employee_id=employee.id,
                    pay_period_start=pay_period_start,
                    pay_period_end=pay_period_end,
                    gross_salary=gross_salary,
                    deductions=other_deductions,
                    net_salary=net_salary,
                    tax_deduction=tax_deduction
                )
                
                crud.create_payroll(db=db, payroll=payroll_data)
                generated_count += 1
        
        return {"message": f"Generated payroll for {generated_count} employees for {year}-{month:02d}"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating payroll: {str(e)}")