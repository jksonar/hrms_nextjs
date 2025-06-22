from fastapi import Depends, HTTPException, status
from app.core.security import get_current_active_user
from app.db.models import User as DBUser, UserRole

def role_required(required_roles: list[UserRole]):
    def _role_checker(current_user: DBUser = Depends(get_current_active_user)):
        if current_user.role not in required_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
        return current_user
    return _role_checker