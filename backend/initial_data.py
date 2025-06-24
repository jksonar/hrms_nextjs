import time
import os
import sys

from app.db import models
from app.db.database import SessionLocal, Base, engine
from app.core.config import settings
from app.schemas.schemas import UserCreate, DepartmentCreate, PositionCreate
from app.services.crud import create_user, create_department, create_position

print(f"Current working directory: {os.getcwd()}")
print(f"DATABASE_URL from settings: {settings.DATABASE_URL}")

def init_db():
    # User model is implicitly imported via schemas.schemas
    # Removed: from db.models import User # Re-add this import here to ensure User is defined within the function scope
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        # Check if admin user exists
        admin_email = settings.ADMIN_EMAIL
        db_admin = db.query(models.User).filter(models.User.email == admin_email).first()
        if not db_admin:
            print("Creating admin user...")
            admin_user = UserCreate(
                email=admin_email,
                password="admin_password",
                is_active=True,
                role="admin"
            )
            create_user(db, admin_user)
            print("Admin user created.")
        else:
            print("Admin user already exists.")

        # Create manager user
        manager_email = "manager@example.com"
        db_manager = db.query(models.User).filter(models.User.email == manager_email).first()
        if not db_manager:
            print("Creating manager user...")
            manager_user = UserCreate(
                email=manager_email,
                password="manager_password",
                is_active=True,
                role="manager"
            )
            create_user(db, manager_user)
            print("Manager user created.")
        else:
            print("Manager user already exists.")

        # Create employee user
        employee_email = "employee@example.com"
        db_employee = db.query(models.User).filter(models.User.email == employee_email).first()
        if not db_employee:
            print("Creating employee user...")
            employee_user = UserCreate(
                email=employee_email,
                password="employee_password",
                is_active=True,
                role="employee"
            )
            create_user(db, employee_user)
            print("Employee user created.")
        else:
            print("Employee user already exists.")

        # Create HR user
        hr_email = "hr@example.com"
        db_hr = db.query(models.User).filter(models.User.email == hr_email).first()
        if not db_hr:
            print("Creating HR user...")
            hr_user = UserCreate(
                email=hr_email,
                password="hr_password",
                is_active=True,
                role="hr"
            )
            create_user(db, hr_user)
            print("HR user created.")
        else:
            print("HR user already exists.")

        # Create sample departments
        departments_data = [
            {"name": "Human Resources", "description": "Manages employee relations and policies"},
            {"name": "Information Technology", "description": "Manages technology infrastructure and development"},
            {"name": "Finance", "description": "Manages financial operations and accounting"},
            {"name": "Marketing", "description": "Manages marketing campaigns and brand promotion"},
            {"name": "Operations", "description": "Manages day-to-day business operations"}
        ]
        
        for dept_data in departments_data:
            existing_dept = db.query(models.Department).filter(models.Department.name == dept_data["name"]).first()
            if not existing_dept:
                print(f"Creating department: {dept_data['name']}")
                department = DepartmentCreate(**dept_data)
                create_department(db, department)
                print(f"Department {dept_data['name']} created.")
            else:
                print(f"Department {dept_data['name']} already exists.")

        # Create sample positions
        positions_data = [
            {"title": "HR Manager", "description": "Manages HR operations", "department_id": 1, "min_salary": 60000, "max_salary": 80000},
            {"title": "HR Specialist", "description": "Handles HR tasks and employee support", "department_id": 1, "min_salary": 40000, "max_salary": 55000},
            {"title": "Software Engineer", "description": "Develops and maintains software applications", "department_id": 2, "min_salary": 70000, "max_salary": 120000},
            {"title": "Senior Software Engineer", "description": "Leads software development projects", "department_id": 2, "min_salary": 90000, "max_salary": 150000},
            {"title": "IT Support Specialist", "description": "Provides technical support", "department_id": 2, "min_salary": 35000, "max_salary": 50000},
            {"title": "Financial Analyst", "description": "Analyzes financial data and trends", "department_id": 3, "min_salary": 50000, "max_salary": 70000},
            {"title": "Accountant", "description": "Manages accounting and bookkeeping", "department_id": 3, "min_salary": 40000, "max_salary": 60000},
            {"title": "Marketing Manager", "description": "Manages marketing strategies", "department_id": 4, "min_salary": 55000, "max_salary": 75000},
            {"title": "Marketing Specialist", "description": "Executes marketing campaigns", "department_id": 4, "min_salary": 35000, "max_salary": 50000},
            {"title": "Operations Manager", "description": "Oversees daily operations", "department_id": 5, "min_salary": 60000, "max_salary": 85000}
        ]
        
        for pos_data in positions_data:
            existing_pos = db.query(models.Position).filter(models.Position.title == pos_data["title"]).first()
            if not existing_pos:
                print(f"Creating position: {pos_data['title']}")
                position = PositionCreate(**pos_data)
                create_position(db, position)
                print(f"Position {pos_data['title']} created.")
            else:
                print(f"Position {pos_data['title']} already exists.")
                
    except Exception as e:
        print(f"Error during database initialization: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    init_db()
    # Removed: time.sleep(2) # Add a small delay
    
    # Print the absolute path of the database file
    if "sqlite:///" in settings.DATABASE_URL:
        db_path = settings.DATABASE_URL.replace("sqlite:///", "")
        print(f"Attempting to connect to absolute path: {os.path.abspath(db_path)}")