#!/usr/bin/env python3

import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.db import models
from app.db.database import SessionLocal
from app.schemas.schemas import DepartmentCreate, PositionCreate
from app.services.crud import create_department, create_position

def populate_sample_data():
    """Populate the database with sample departments and positions."""
    db = SessionLocal()
    try:
        print("Populating sample departments and positions...")
        
        # Create sample departments
        departments_data = [
            {"name": "Human Resources", "description": "Manages employee relations and policies"},
            {"name": "Information Technology", "description": "Manages technology infrastructure and development"},
            {"name": "Finance", "description": "Manages financial operations and accounting"},
            {"name": "Marketing", "description": "Manages marketing campaigns and brand promotion"},
            {"name": "Operations", "description": "Manages day-to-day business operations"}
        ]
        
        created_departments = []
        for dept_data in departments_data:
            existing_dept = db.query(models.Department).filter(models.Department.name == dept_data["name"]).first()
            if not existing_dept:
                print(f"Creating department: {dept_data['name']}")
                department = DepartmentCreate(**dept_data)
                new_dept = create_department(db, department)
                created_departments.append(new_dept)
                print(f"Department {dept_data['name']} created with ID: {new_dept.id}")
            else:
                print(f"Department {dept_data['name']} already exists with ID: {existing_dept.id}")
                created_departments.append(existing_dept)

        # Get department IDs for positions
        hr_dept = db.query(models.Department).filter(models.Department.name == "Human Resources").first()
        it_dept = db.query(models.Department).filter(models.Department.name == "Information Technology").first()
        finance_dept = db.query(models.Department).filter(models.Department.name == "Finance").first()
        marketing_dept = db.query(models.Department).filter(models.Department.name == "Marketing").first()
        ops_dept = db.query(models.Department).filter(models.Department.name == "Operations").first()

        # Create sample positions
        positions_data = [
            {"title": "HR Manager", "description": "Manages HR operations", "department_id": hr_dept.id if hr_dept else None, "min_salary": 60000, "max_salary": 80000},
            {"title": "HR Specialist", "description": "Handles HR tasks and employee support", "department_id": hr_dept.id if hr_dept else None, "min_salary": 40000, "max_salary": 55000},
            {"title": "Software Engineer", "description": "Develops and maintains software applications", "department_id": it_dept.id if it_dept else None, "min_salary": 70000, "max_salary": 120000},
            {"title": "Senior Software Engineer", "description": "Leads software development projects", "department_id": it_dept.id if it_dept else None, "min_salary": 90000, "max_salary": 150000},
            {"title": "IT Support Specialist", "description": "Provides technical support", "department_id": it_dept.id if it_dept else None, "min_salary": 35000, "max_salary": 50000},
            {"title": "Financial Analyst", "description": "Analyzes financial data and trends", "department_id": finance_dept.id if finance_dept else None, "min_salary": 50000, "max_salary": 70000},
            {"title": "Accountant", "description": "Manages accounting and bookkeeping", "department_id": finance_dept.id if finance_dept else None, "min_salary": 40000, "max_salary": 60000},
            {"title": "Marketing Manager", "description": "Manages marketing strategies", "department_id": marketing_dept.id if marketing_dept else None, "min_salary": 55000, "max_salary": 75000},
            {"title": "Marketing Specialist", "description": "Executes marketing campaigns", "department_id": marketing_dept.id if marketing_dept else None, "min_salary": 35000, "max_salary": 50000},
            {"title": "Operations Manager", "description": "Oversees daily operations", "department_id": ops_dept.id if ops_dept else None, "min_salary": 60000, "max_salary": 85000}
        ]
        
        for pos_data in positions_data:
            existing_pos = db.query(models.Position).filter(models.Position.title == pos_data["title"]).first()
            if not existing_pos:
                print(f"Creating position: {pos_data['title']}")
                position = PositionCreate(**pos_data)
                new_pos = create_position(db, position)
                print(f"Position {pos_data['title']} created with ID: {new_pos.id}")
            else:
                print(f"Position {pos_data['title']} already exists with ID: {existing_pos.id}")
                
        print("\nSample data population completed!")
        print("\nAvailable departments:")
        departments = db.query(models.Department).all()
        for dept in departments:
            print(f"  - {dept.name} (ID: {dept.id})")
            
        print("\nAvailable positions:")
        positions = db.query(models.Position).all()
        for pos in positions:
            print(f"  - {pos.title} (ID: {pos.id}) - Department: {pos.department_id}")
                
    except Exception as e:
        print(f"Error during sample data population: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    populate_sample_data()