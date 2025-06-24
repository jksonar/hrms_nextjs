'use client';

import React from 'react';
import { usePermissions } from '@/hooks/usePermissions';
import { Permission } from '@/types/permissions';
import { UserRole } from '@/types';

interface ProtectedComponentProps {
  children: React.ReactNode;
  fallback?: React.ReactNode;
  // Permission-based protection
  permission?: Permission;
  permissions?: Permission[];
  requireAll?: boolean; // If true, requires all permissions; if false, requires any permission
  // Role-based protection (legacy support)
  roles?: UserRole[];
}

export const ProtectedComponent: React.FC<ProtectedComponentProps> = ({
  children,
  fallback = null,
  permission,
  permissions,
  requireAll = false,
  roles,
}) => {
  const { hasPermission, hasAnyPermission, hasAllPermissions, userRole } = usePermissions();
  
  let hasAccess = false;
  
  // Check single permission
  if (permission) {
    hasAccess = hasPermission(permission);
  }
  // Check multiple permissions
  else if (permissions && permissions.length > 0) {
    hasAccess = requireAll 
      ? hasAllPermissions(permissions)
      : hasAnyPermission(permissions);
  }
  // Fallback to role-based check (legacy support)
  else if (roles && roles.length > 0 && userRole) {
    hasAccess = roles.includes(userRole);
  }
  // If no restrictions specified, allow access
  else {
    hasAccess = true;
  }
  
  return hasAccess ? <>{children}</> : <>{fallback}</>;
};

// Convenience components for common use cases
export const AdminOnly: React.FC<{ children: React.ReactNode; fallback?: React.ReactNode }> = ({
  children,
  fallback = null,
}) => (
  <ProtectedComponent roles={[UserRole.ADMIN]} fallback={fallback}>
    {children}
  </ProtectedComponent>
);

export const HROnly: React.FC<{ children: React.ReactNode; fallback?: React.ReactNode }> = ({
  children,
  fallback = null,
}) => (
  <ProtectedComponent roles={[UserRole.ADMIN, UserRole.HR]} fallback={fallback}>
    {children}
  </ProtectedComponent>
);

export const ManagerAndAbove: React.FC<{ children: React.ReactNode; fallback?: React.ReactNode }> = ({
  children,
  fallback = null,
}) => (
  <ProtectedComponent roles={[UserRole.ADMIN, UserRole.HR, UserRole.MANAGER]} fallback={fallback}>
    {children}
  </ProtectedComponent>
);