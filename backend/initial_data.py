import time
import os
import sys

from app.db import models
from app.db.database import SessionLocal, Base, engine
from app.core.config import settings
from app.schemas.schemas import UserCreate
from app.services.crud import create_user

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