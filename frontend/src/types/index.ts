// User types
export interface User {
  id: number;
  email: string;
  full_name: string;
  role: UserRole;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface UserCreate {
  email: string;
  password: string;
  full_name: string;
  role?: UserRole;
}

export interface UserUpdate {
  email?: string;
  full_name?: string;
  role?: UserRole;
  is_active?: boolean;
}

export enum UserRole {
  ADMIN = 'admin',
  HR = 'hr',
  MANAGER = 'manager',
  EMPLOYEE = 'employee',
}

// Employee types
export interface Employee {
  id: number;
  user_id: number;
  employee_id: string;
  first_name: string;
  last_name: string;
  email: string;
  phone: string;
  hire_date: string;
  department_id: number;
  position_id: number;
  salary: number;
  is_active: boolean;
  created_at: string;
  updated_at: string;
  user?: User;
  department?: Department;
  position?: Position;
}

export interface EmployeeCreate {
  user_id: number;
  employee_id: string;
  first_name: string;
  last_name: string;
  email: string;
  phone: string;
  hire_date: string;
  department_id: number;
  position_id: number;
  salary: number;
}

export interface EmployeeUpdate {
  employee_id?: string;
  first_name?: string;
  last_name?: string;
  email?: string;
  phone?: string;
  hire_date?: string;
  department_id?: number;
  position_id?: number;
  salary?: number;
  is_active?: boolean;
}

// Department types
export interface Department {
  id: number;
  name: string;
  description: string;
  manager_id?: number;
  created_at: string;
  updated_at: string;
  manager?: Employee;
}

export interface DepartmentCreate {
  name: string;
  description: string;
  manager_id?: number;
}

export interface DepartmentUpdate {
  name?: string;
  description?: string;
  manager_id?: number;
}

// Export CreateDepartment as alias for DepartmentCreate
export type CreateDepartment = DepartmentCreate;

// Position types
export interface Position {
  id: number;
  title: string;
  description: string;
  department_id: number;
  salary_min?: number;
  salary_max?: number;
  created_at: string;
  updated_at: string;
  department?: Department;
}

export interface PositionCreate {
  title: string;
  description: string;
  department_id: number;
}

export interface PositionUpdate {
  title?: string;
  description?: string;
  department_id?: number;
}

// Export CreatePosition as alias for PositionCreate
export type CreatePosition = PositionCreate;

// Attendance types
export interface Attendance {
  id: number;
  employee_id: number;
  date: string;
  clock_in_time: string;
  clock_out_time?: string;
  break_start?: string;
  break_end?: string;
  total_hours?: number;
  overtime_hours?: number;
  status: AttendanceStatus;
  created_at: string;
  updated_at: string;
  employee?: Employee;
}

export interface AttendanceCreate {
  employee_id: number;
  date: string;
  clock_in: string;
  clock_out?: string;
  break_start?: string;
  break_end?: string;
  status?: AttendanceStatus;
}

export interface AttendanceUpdate {
  clock_in?: string;
  clock_out?: string;
  break_start?: string;
  break_end?: string;
  status?: AttendanceStatus;
}

export enum AttendanceStatus {
  PRESENT = 'present',
  ABSENT = 'absent',
  LATE = 'late',
  HALF_DAY = 'half_day',
}

// Leave Request types
export interface LeaveRequest {
  id: number;
  employee_id: number;
  leave_type: LeaveType;
  start_date: string;
  end_date: string;
  days_requested: number;
  reason: string;
  status: LeaveStatus;
  approved_by?: number;
  approved_at?: string;
  comments?: string;
  created_at: string;
  updated_at: string;
  employee?: Employee;
  approver?: Employee;
}

export interface LeaveRequestCreate {
  employee_id: number;
  leave_type: LeaveType;
  start_date: string;
  end_date: string;
  reason: string;
}

export interface LeaveRequestUpdate {
  leave_type?: LeaveType;
  start_date?: string;
  end_date?: string;
  reason?: string;
  status?: LeaveStatus;
  comments?: string;
}

// Export CreateLeaveRequest as alias for LeaveRequestCreate
export type CreateLeaveRequest = LeaveRequestCreate;

export enum LeaveType {
  ANNUAL = 'annual',
  SICK = 'sick',
  MATERNITY = 'maternity',
  PATERNITY = 'paternity',
  PERSONAL = 'personal',
  EMERGENCY = 'emergency',
}

export enum LeaveStatus {
  PENDING = 'pending',
  APPROVED = 'approved',
  REJECTED = 'rejected',
  CANCELLED = 'cancelled',
}

// Payroll types
export interface Payroll {
  id: number;
  employee_id: number;
  pay_period_start: string;
  pay_period_end: string;
  basic_salary: number;
  overtime_pay: number;
  bonus: number;
  allowances: number;
  deductions: number;
  gross_pay: number;
  tax_deduction: number;
  net_pay: number;
  pay_date: string;
  status: PayrollStatus;
  created_at: string;
  updated_at: string;
  employee?: Employee;
}

export interface PayrollCreate {
  employee_id: number;
  pay_period_start: string;
  pay_period_end: string;
  basic_salary: number;
  overtime_pay?: number;
  bonus?: number;
  deductions?: number;
  tax_deduction?: number;
  pay_date: string;
}

export interface PayrollUpdate {
  basic_salary?: number;
  overtime_pay?: number;
  bonus?: number;
  deductions?: number;
  tax_deduction?: number;
  pay_date?: string;
  status?: PayrollStatus;
}

export enum PayrollStatus {
  DRAFT = 'draft',
  PROCESSED = 'processed',
  PAID = 'paid',
}

// Auth types
export interface LoginCredentials {
  email: string;
  password: string;
}

export interface AuthResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

// API Response types
export interface ApiResponse<T> {
  data: T;
  message?: string;
  status: number;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  size: number;
  pages: number;
}

// Dashboard types
export interface DashboardStats {
  totalEmployees: number;
  totalDepartments: number;
  pendingLeaveRequests: number;
  todayAttendance: number;
  monthlyPayroll: number;
}

// Form types
export interface FormField {
  name: string;
  label: string;
  type: 'text' | 'email' | 'password' | 'number' | 'date' | 'select' | 'textarea';
  required?: boolean;
  options?: { value: string | number; label: string }[];
  placeholder?: string;
  validation?: any;
}