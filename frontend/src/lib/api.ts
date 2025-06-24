import axios from 'axios';
import Cookies from 'js-cookie';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = Cookies.get('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle token expiration
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      Cookies.remove('access_token');
      Cookies.remove('refresh_token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  login: (credentials: { email: string; password: string }) =>
    api.post('/login', credentials),
  register: (userData: { email: string; password: string; full_name: string }) =>
    api.post('/register', userData),
  getCurrentUser: () => api.get('/users/me'),
  logout: () => {
    Cookies.remove('access_token');
    Cookies.remove('refresh_token');
  },
};

// Users API
export const usersAPI = {
  getUsers: (skip = 0, limit = 100) =>
    api.get(`/users/?skip=${skip}&limit=${limit}`),
  getUser: (userId: number) => api.get(`/users/${userId}`),
  updateUser: (userId: number, userData: any) =>
    api.put(`/users/${userId}`, userData),
  deleteUser: (userId: number) => api.delete(`/users/${userId}`),
};

// Employees API
export const employeesAPI = {
  getEmployees: (skip = 0, limit = 100) =>
    api.get(`/employees/?skip=${skip}&limit=${limit}`),
  getEmployee: (employeeId: number) => api.get(`/employees/${employeeId}`),
  createEmployee: (employeeData: any) => api.post('/employees/', employeeData),
  updateEmployee: (employeeId: number, employeeData: any) =>
    api.put(`/employees/${employeeId}`, employeeData),
  deleteEmployee: (employeeId: number) => api.delete(`/employees/${employeeId}`),
  // Alias methods for backward compatibility
  getAll: (skip = 0, limit = 100) =>
    api.get(`/employees/?skip=${skip}&limit=${limit}`),
};

// Departments API
export const departmentsAPI = {
  getDepartments: (skip = 0, limit = 100) =>
    api.get(`/departments/?skip=${skip}&limit=${limit}`),
  getDepartment: (departmentId: number) => api.get(`/departments/${departmentId}`),
  createDepartment: (departmentData: any) =>
    api.post('/departments/', departmentData),
  updateDepartment: (departmentId: number, departmentData: any) =>
    api.put(`/departments/${departmentId}`, departmentData),
  deleteDepartment: (departmentId: number) =>
    api.delete(`/departments/${departmentId}`),
  // Alias methods for backward compatibility
  getAll: (skip = 0, limit = 100) =>
    api.get(`/departments/?skip=${skip}&limit=${limit}`),
  create: (departmentData: any) => api.post('/departments/', departmentData),
  update: (departmentId: number, departmentData: any) =>
    api.put(`/departments/${departmentId}`, departmentData),
  delete: (departmentId: number) => api.delete(`/departments/${departmentId}`),
};

// Positions API
export const positionsAPI = {
  getPositions: (skip = 0, limit = 100) =>
    api.get(`/positions/?skip=${skip}&limit=${limit}`),
  getPosition: (positionId: number) => api.get(`/positions/${positionId}`),
  createPosition: (positionData: any) => api.post('/positions/', positionData),
  updatePosition: (positionId: number, positionData: any) =>
    api.put(`/positions/${positionId}`, positionData),
  deletePosition: (positionId: number) => api.delete(`/positions/${positionId}`),
};

// Attendance API
export const attendanceAPI = {
  getAttendance: (skip = 0, limit = 100) =>
    api.get(`/attendance/?skip=${skip}&limit=${limit}`),
  getEmployeeAttendance: (employeeId: number, skip = 0, limit = 100) =>
    api.get(`/attendance/employee/${employeeId}?skip=${skip}&limit=${limit}`),
  createAttendance: (attendanceData: any) =>
    api.post('/attendance/', attendanceData),
  updateAttendance: (attendanceId: number, attendanceData: any) =>
    api.put(`/attendance/${attendanceId}`, attendanceData),
  deleteAttendance: (attendanceId: number) =>
    api.delete(`/attendance/${attendanceId}`),
  clockIn: (employeeId?: number) =>
    api.post('/attendance/clock-in', employeeId ? { employee_id: employeeId } : {}),
  clockOut: (employeeId: number) =>
    api.post('/attendance/clock-out', { employee_id: employeeId }),
  // Alias methods for backward compatibility
  getAll: (skip = 0, limit = 100) =>
    api.get(`/attendance/?skip=${skip}&limit=${limit}`),
  getByEmployee: (employeeId: number, startDate?: string, endDate?: string) => {
    let url = `/attendance/employee/${employeeId}`;
    const params = new URLSearchParams();
    if (startDate) params.append('start_date', startDate);
    if (endDate) params.append('end_date', endDate);
    if (params.toString()) url += `?${params.toString()}`;
    return api.get(url);
  },
};

// Leave Requests API
export const leaveRequestsAPI = {
  getLeaveRequests: (skip = 0, limit = 100) =>
    api.get(`/leave-requests/?skip=${skip}&limit=${limit}`),
  getEmployeeLeaveRequests: (employeeId: number) =>
    api.get(`/leave-requests/employee/${employeeId}`),
  createLeaveRequest: (leaveData: any) =>
    api.post('/leave-requests/', leaveData),
  updateLeaveRequest: (leaveId: number, leaveData: any) =>
    api.put(`/leave-requests/${leaveId}`, leaveData),
  approveLeaveRequest: (leaveId: number) =>
    api.put(`/leave-requests/${leaveId}/approve`),
  rejectLeaveRequest: (leaveId: number) =>
    api.put(`/leave-requests/${leaveId}/reject`),
  // Alias methods for backward compatibility
  getAll: () => leaveRequestsAPI.getLeaveRequests(),
  getByEmployee: (employeeId: number) => leaveRequestsAPI.getEmployeeLeaveRequests(employeeId),
  approve: (id: number) => api.put(`/leave-requests/${id}/approve`),
  reject: (id: number, reason: string) => api.put(`/leave-requests/${id}/reject`, { reason }),
};

// Payroll API
export const payrollAPI = {
  getPayroll: (skip = 0, limit = 100) =>
    api.get(`/payroll/?skip=${skip}&limit=${limit}`),
  getEmployeePayroll: (employeeId: number, skip = 0, limit = 100) =>
    api.get(`/payroll/employee/${employeeId}?skip=${skip}&limit=${limit}`),
  createPayroll: (payrollData: any) => api.post('/payroll/', payrollData),
  updatePayroll: (payrollId: number, payrollData: any) =>
    api.put(`/payroll/${payrollId}`, payrollData),
  deletePayroll: (payrollId: number) => api.delete(`/payroll/${payrollId}`),
  generatePayslip: (payrollId: number) =>
    api.get(`/payroll/${payrollId}/payslip`, { responseType: 'blob' }),
  // Alias methods for backward compatibility
  getAll: (skip = 0, limit = 100) =>
    api.get(`/payroll/?skip=${skip}&limit=${limit}`),
  getByEmployee: (employeeId: number, skip = 0, limit = 100) =>
    api.get(`/payroll/employee/${employeeId}?skip=${skip}&limit=${limit}`),
};

export default api;