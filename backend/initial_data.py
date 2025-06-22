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