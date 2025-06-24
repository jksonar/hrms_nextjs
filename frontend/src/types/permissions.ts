export enum Permission {
  // Employee permissions
  CREATE_EMPLOYEE = 'create_employee',
  READ_EMPLOYEE = 'read_employee',
  UPDATE_EMPLOYEE = 'update_employee',
  DELETE_EMPLOYEE = 'delete_employee',
  
  // Department permissions
  CREATE_DEPARTMENT = 'create_department',
  READ_DEPARTMENT = 'read_department',
  UPDATE_DEPARTMENT = 'update_department',
  DELETE_DEPARTMENT = 'delete_department',
  
  // Attendance permissions
  CREATE_ATTENDANCE = 'create_attendance',
  READ_ATTENDANCE = 'read_attendance',
  UPDATE_ATTENDANCE = 'update_attendance',
  DELETE_ATTENDANCE = 'delete_attendance',
  
  // Leave permissions
  CREATE_LEAVE_REQUEST = 'create_leave_request',
  READ_LEAVE_REQUEST = 'read_leave_request',
  UPDATE_LEAVE_REQUEST = 'update_leave_request',
  DELETE_LEAVE_REQUEST = 'delete_leave_request',
  APPROVE_LEAVE_REQUEST = 'approve_leave_request',
  REJECT_LEAVE_REQUEST = 'reject_leave_request',
  
  // Payroll permissions
  CREATE_PAYROLL = 'create_payroll',
  READ_PAYROLL = 'read_payroll',
  UPDATE_PAYROLL = 'update_payroll',
  DELETE_PAYROLL = 'delete_payroll',
  
  // User permissions
  CREATE_USER = 'create_user',
  READ_USER = 'read_user',
  UPDATE_USER = 'update_user',
  DELETE_USER = 'delete_user',
  
  // System permissions
  ACCESS_REPORTS = 'access_reports',
  ACCESS_SETTINGS = 'access_settings',
  MANAGE_ROLES = 'manage_roles',
}