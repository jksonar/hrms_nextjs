from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime

from app.db.database import get_db
from app.db.models import User as DBUser, AuditLog
from app.core.security import get_current_active_user
from app.core.security import role_required
from app.db.models import UserRole
from app.services.audit import get_audit_logs
from pydantic import BaseModel

router = APIRouter()

class AuditLogResponse(BaseModel):
    id: int
    user_id: int
    action: str
    resource: str
    resource_id: Optional[int]
    details: Optional[dict]
    ip_address: Optional[str]
    user_agent: Optional[str]
    timestamp: datetime
    user_email: Optional[str]
    
    class Config:
        from_attributes = True

@router.get("/", response_model=List[AuditLogResponse])
def read_audit_logs(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    user_id: Optional[int] = Query(None),
    action: Optional[str] = Query(None),
    resource: Optional[str] = Query(None),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(role_required([UserRole.ADMIN]))
):
    """
    Retrieve audit logs with optional filtering.
    Only accessible by administrators.
    """
    audit_logs = get_audit_logs(
        db=db,
        skip=skip,
        limit=limit,
        user_id=user_id,
        action=action,
        resource=resource,
        start_date=start_date,
        end_date=end_date
    )
    
    # Add user email to each audit log for better readability
    result = []
    for log in audit_logs:
        log_dict = {
            "id": log.id,
            "user_id": log.user_id,
            "action": log.action,
            "resource": log.resource,
            "resource_id": log.resource_id,
            "details": log.details,
            "ip_address": log.ip_address,
            "user_agent": log.user_agent,
            "timestamp": log.timestamp,
            "user_email": log.user.email if log.user else None
        }
        result.append(AuditLogResponse(**log_dict))
    
    return result

@router.get("/stats", response_model=dict)
def get_audit_stats(
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(role_required([UserRole.ADMIN]))
):
    """
    Get audit log statistics.
    Only accessible by administrators.
    """
    query = db.query(AuditLog)
    
    if start_date:
        query = query.filter(AuditLog.timestamp >= start_date)
    if end_date:
        query = query.filter(AuditLog.timestamp <= end_date)
    
    total_logs = query.count()
    
    # Count by action
    action_counts = {}
    for action, count in query.with_entities(AuditLog.action, db.func.count(AuditLog.id)).group_by(AuditLog.action).all():
        action_counts[action] = count
    
    # Count by resource
    resource_counts = {}
    for resource, count in query.with_entities(AuditLog.resource, db.func.count(AuditLog.id)).group_by(AuditLog.resource).all():
        resource_counts[resource] = count
    
    # Count by user
    user_counts = {}
    for user_id, count in query.with_entities(AuditLog.user_id, db.func.count(AuditLog.id)).group_by(AuditLog.user_id).all():
        user = db.query(DBUser).filter(DBUser.id == user_id).first()
        user_email = user.email if user else f"User {user_id}"
        user_counts[user_email] = count
    
    return {
        "total_logs": total_logs,
        "action_counts": action_counts,
        "resource_counts": resource_counts,
        "user_counts": user_counts,
        "date_range": {
            "start_date": start_date,
            "end_date": end_date
        }
    }