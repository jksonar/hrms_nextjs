import { UserRole } from '@/types';
import { Permission } from '@/types/permissions';

export const rolePermissions: Record<UserRole, Permission[]> = {
  [UserRole.ADMIN]: [
    // All permissions for admin
    Permission.CREATE_EMPLOYEE,
    Permission.READ_EMPLOYEE,
    Permission.UPDATE_EMPLOYEE,
    Permission.DELETE_EMPLOYEE,
    Permission.CREATE_DEPARTMENT,
    Permission.READ_DEPARTMENT,
    Permission.UPDATE_DEPARTMENT,
    Permission.DELETE_DEPARTMENT,
    Permission.CREATE_ATTENDANCE,
    Permission.READ_ATTENDANCE,
    Permission.UPDATE_ATTENDANCE,
    Permission.DELETE_ATTENDANCE,
    Permission.CREATE_LEAVE_REQUEST,
    Permission.READ_LEAVE_REQUEST,
    Permission.UPDATE_LEAVE_REQUEST,
    Permission.DELETE_LEAVE_REQUEST,
    Permission.APPROVE_LEAVE_REQUEST,
    Permission.REJECT_LEAVE_REQUEST,
    Permission.CREATE_PAYROLL,
    Permission.READ_PAYROLL,
    Permission.UPDATE_PAYROLL,
    Permission.DELETE_PAYROLL,
    Permission.CREATE_USER,
    Permission.READ_USER,
    Permission.UPDATE_USER,
    Permission.DELETE_USER,
    Permission.ACCESS_REPORTS,
    Permission.ACCESS_SETTINGS,
    Permission.MANAGE_ROLES,
  ],
  
  [UserRole.HR]: [
    // HR permissions
    Permission.CREATE_EMPLOYEE,
    Permission.READ_EMPLOYEE,
    Permission.UPDATE_EMPLOYEE,
    Permission.CREATE_DEPARTMENT,
    Permission.READ_DEPARTMENT,
    Permission.UPDATE_DEPARTMENT,
    Permission.READ_ATTENDANCE,
    Permission.UPDATE_ATTENDANCE,
    Permission.READ_LEAVE_REQUEST,
    Permission.UPDATE_LEAVE_REQUEST,
    Permission.APPROVE_LEAVE_REQUEST,
    Permission.REJECT_LEAVE_REQUEST,
    Permission.CREATE_PAYROLL,
    Permission.READ_PAYROLL,
    Permission.UPDATE_PAYROLL,
    Permission.READ_USER,
    Permission.ACCESS_REPORTS,
  ],
  
  [UserRole.MANAGER]: [
    // Manager permissions
    Permission.READ_EMPLOYEE,
    Permission.UPDATE_EMPLOYEE, // Limited to their team
    Permission.READ_DEPARTMENT,
    Permission.CREATE_ATTENDANCE,
    Permission.READ_ATTENDANCE,
    Permission.UPDATE_ATTENDANCE,
    Permission.READ_LEAVE_REQUEST,
    Permission.APPROVE_LEAVE_REQUEST, // Limited to their team
    Permission.REJECT_LEAVE_REQUEST, // Limited to their team
    Permission.READ_USER,
    Permission.ACCESS_REPORTS, // Limited to their team
  ],
  
  [UserRole.EMPLOYEE]: [
    // Employee permissions
    Permission.READ_EMPLOYEE, // Limited to self
    Permission.UPDATE_EMPLOYEE, // Limited to self
    Permission.CREATE_ATTENDANCE, // Limited to self
    Permission.READ_ATTENDANCE, // Limited to self
    Permission.CREATE_LEAVE_REQUEST,
    Permission.READ_LEAVE_REQUEST, // Limited to self
    Permission.UPDATE_LEAVE_REQUEST, // Limited to self
    Permission.READ_PAYROLL, // Limited to self
    Permission.READ_USER, // Limited to self
  ],
};

export const hasPermission = (userRole: UserRole | undefined, permission: Permission): boolean => {
  if (!userRole) return false;
  return rolePermissions[userRole]?.includes(permission) || false;
};

export const hasAnyPermission = (userRole: UserRole | undefined, permissions: Permission[]): boolean => {
  if (!userRole) return false;
  return permissions.some(permission => hasPermission(userRole, permission));
};

export const hasAllPermissions = (userRole: UserRole | undefined, permissions: Permission[]): boolean => {
  if (!userRole) return false;
  return permissions.every(permission => hasPermission(userRole, permission));
};