import json
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from fastapi import Request
from app.db.models import AuditLog, User
from app.services import crud

def log_action(
    db: Session,
    user: User,
    action: str,
    resource: str,
    resource_id: Optional[int] = None,
    details: Optional[Dict[str, Any]] = None,
    request: Optional[Request] = None
) -> AuditLog:
    """
    Log a user action for audit purposes.
    
    Args:
        db: Database session
        user: User performing the action
        action: Action type (CREATE, READ, UPDATE, DELETE)
        resource: Resource type (employees, departments, etc.)
        resource_id: ID of the affected resource
        details: Additional details about the action
        request: FastAPI request object for IP and user agent
    
    Returns:
        Created AuditLog instance
    """
    ip_address = None
    user_agent = None
    
    if request:
        # Get client IP address
        ip_address = request.client.host if request.client else None
        # Handle X-Forwarded-For header for proxied requests
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            ip_address = forwarded_for.split(",")[0].strip()
        
        # Get user agent
        user_agent = request.headers.get("User-Agent")
    
    audit_log = AuditLog(
        user_id=user.id,
        action=action.upper(),
        resource=resource.lower(),
        resource_id=resource_id,
        details=json.dumps(details) if details else None,
        ip_address=ip_address,
        user_agent=user_agent
    )
    
    db.add(audit_log)
    db.commit()
    db.refresh(audit_log)
    
    return audit_log

def log_create(db: Session, user: User, resource: str, resource_id: int, details: Optional[Dict[str, Any]] = None, request: Optional[Request] = None):
    """Log a CREATE action."""
    return log_action(db, user, "CREATE", resource, resource_id, details, request)

def log_read(db: Session, user: User, resource: str, resource_id: Optional[int] = None, details: Optional[Dict[str, Any]] = None, request: Optional[Request] = None):
    """Log a READ action."""
    return log_action(db, user, "READ", resource, resource_id, details, request)

def log_update(db: Session, user: User, resource: str, resource_id: int, details: Optional[Dict[str, Any]] = None, request: Optional[Request] = None):
    """Log an UPDATE action."""
    return log_action(db, user, "UPDATE", resource, resource_id, details, request)

def log_delete(db: Session, user: User, resource: str, resource_id: int, details: Optional[Dict[str, Any]] = None, request: Optional[Request] = None):
    """Log a DELETE action."""
    return log_action(db, user, "DELETE", resource, resource_id, details, request)

def log_login(db: Session, user: User, request: Optional[Request] = None):
    """Log a successful login."""
    return log_action(db, user, "LOGIN", "auth", user.id, {"email": user.email}, request)

def log_logout(db: Session, user: User, request: Optional[Request] = None):
    """Log a logout."""
    return log_action(db, user, "LOGOUT", "auth", user.id, {"email": user.email}, request)

def log_failed_login(db: Session, email: str, request: Optional[Request] = None):
    """Log a failed login attempt."""
    # Create a temporary audit log without user_id for failed attempts
    ip_address = None
    user_agent = None
    
    if request:
        ip_address = request.client.host if request.client else None
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            ip_address = forwarded_for.split(",")[0].strip()
        user_agent = request.headers.get("User-Agent")
    
    # For failed logins, we don't have a user_id, so we'll use a special approach
    # You might want to create a separate table for failed login attempts
    # For now, we'll skip logging failed attempts to avoid foreign key issues
    pass

def get_audit_logs(
    db: Session,
    user_id: Optional[int] = None,
    resource: Optional[str] = None,
    action: Optional[str] = None,
    skip: int = 0,
    limit: int = 100
) -> list[AuditLog]:
    """Retrieve audit logs with optional filtering."""
    query = db.query(AuditLog)
    
    if user_id:
        query = query.filter(AuditLog.user_id == user_id)
    if resource:
        query = query.filter(AuditLog.resource == resource.lower())
    if action:
        query = query.filter(AuditLog.action == action.upper())
    
    return query.order_by(AuditLog.timestamp.desc()).offset(skip).limit(limit).all()