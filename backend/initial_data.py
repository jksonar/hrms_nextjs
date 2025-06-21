import os
import sys
from sqlalchemy.orm import Session

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.database import SessionLocal
from app.db.models import User, UserRole
from app.core.hashing import get_password_hash
from app.services import crud


def create_initial_admin_user(db: Session):
    admin_email = os.getenv("ADMIN_EMAIL", "admin@example.com")
    admin_password = os.getenv("ADMIN_PASSWORD", "adminpass")

    user = crud.get_user_by_email(db, email=admin_email)
    if not user:
        print(f"Creating initial admin user: {admin_email}")
        user_in = {"email": admin_email, "password": admin_password, "role": UserRole.ADMIN}
        crud.create_user(db, user_in)
        print("Admin user created successfully.")
    else:
        print(f"Admin user {admin_email} already exists.")

if __name__ == "__main__":
    db = SessionLocal()
    try:
        create_initial_admin_user(db)
    finally:
        db.close()