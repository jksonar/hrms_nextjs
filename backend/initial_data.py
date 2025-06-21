import time
import os
import sys

# Add the parent directory to the sys.path to allow imports from the app module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'app')))

import db.models # Re-add this import at the top level

from db.database import SessionLocal
from core.config import settings
from schemas.schemas import UserCreate
from services.crud import create_user

print(f"Current working directory: {os.getcwd()}")
print(f"DATABASE_URL from settings: {settings.DATABASE_URL}")

def init_db():
    # User model is implicitly imported via schemas.schemas
    # Removed: from db.models import User # Re-add this import here to ensure User is defined within the function scope
    db = SessionLocal()
    try:
        # Check if admin user exists
        admin_email = settings.ADMIN_EMAIL
        db_admin = db.query(db.models.User).filter(db.models.User.email == admin_email).first()
        if not db_admin:
            print("Creating admin user...")
            admin_user = UserCreate(
                email=admin_email,
                password="admin_password", # Placeholder, as ADMIN_PASSWORD is not in config
                is_active=True,
                role="admin"
            )
            create_user(db, admin_user)
            print("Admin user created.")
        else:
            print("Admin user already exists.")
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