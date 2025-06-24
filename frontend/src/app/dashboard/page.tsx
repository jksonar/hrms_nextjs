'use client';

import { useEffect, useState } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import {
  UsersIcon,
  BuildingOfficeIcon,
  DocumentTextIcon,
  ClockIcon,
  CurrencyDollarIcon,
} from '@heroicons/react/24/outline';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
} from 'recharts';
import { employeesAPI, departmentsAPI, leaveRequestsAPI, attendanceAPI } from '@/lib/api';
import { DashboardStats } from '@/types';

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042'];

interface StatCardProps {
  title: string;
  value: string | number;
  icon: React.ComponentType<React.SVGProps<SVGSVGElement>>;
  color: string;
  change?: string;
}

function StatCard({ title, value, icon: Icon, color, change }: StatCardProps) {
  return (
    <div className="bg-white overflow-hidden shadow rounded-lg">
      <div className="p-5">
        <div className="flex items-center">
          <div className="flex-shrink-0">
            <Icon className={`h-6 w-6 ${color}`} />
          </div>
          <div className="ml-5 w-0 flex-1">
            <dl>
              <dt className="text-sm font-medium text-gray-500 truncate">{title}</dt>
              <dd className="text-lg font-medium text-gray-900">{value}</dd>
            </dl>
          </div>
        </div>
        {change && (
          <div className="mt-3">
            <span className="text-sm text-gray-500">{change}</span>
          </div>
        )}
      </div>
    </div>
  );
}

export default function DashboardPage() {
  const { user } = useAuth();
  const [stats, setStats] = useState<DashboardStats>({
    totalEmployees: 0,
    totalDepartments: 0,
    pendingLeaveRequests: 0,
    todayAttendance: 0,
    monthlyPayroll: 0,
  });
  const [loading, setLoading] = useState(true);
  const [attendanceData, setAttendanceData] = useState<any[]>([]);
  const [departmentData, setDepartmentData] = useState<any[]>([]);

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        setLoading(true);
        
        // Fetch employees
        const employeesResponse = await employeesAPI.getEmployees(0, 100);
        const employees = employeesResponse.data;
        
        // Fetch departments
        const departmentsResponse = await departmentsAPI.getDepartments(0, 100);
        const departments = departmentsResponse.data;
        
        // Fetch leave requests
        const leaveRequestsResponse = await leaveRequestsAPI.getLeaveRequests(0, 100);
        const leaveRequests = leaveRequestsResponse.data;
        const pendingLeaves = leaveRequests.filter((req: any) => req.status === 'pending');
        
        // Mock attendance data for chart
        const mockAttendanceData = [
          { name: 'Mon', present: 85, absent: 15 },
          { name: 'Tue', present: 88, absent: 12 },
          { name: 'Wed', present: 82, absent: 18 },
          { name: 'Thu', present: 90, absent: 10 },
          { name: 'Fri', present: 87, absent: 13 },
          { name: 'Sat', present: 45, absent: 55 },
          { name: 'Sun', present: 20, absent: 80 },
        ];
        
        // Mock department distribution
        const mockDepartmentData = departments.map((dept: any, index: number) => ({
          name: dept.name,
          value: Math.floor(Math.random() * 20) + 5,
          color: COLORS[index % COLORS.length],
        }));
        
        setStats({
          totalEmployees: employees.length,
          totalDepartments: departments.length,
          pendingLeaveRequests: pendingLeaves.length,
          todayAttendance: 85, // Mock data
          monthlyPayroll: 125000, // Mock data
        });
        
        setAttendanceData(mockAttendanceData);
        setDepartmentData(mockDepartmentData);
      } catch (error) {
        console.error('Error fetching dashboard data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardData();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-semibold text-gray-900">
          Welcome back, {user?.full_name}!
        </h1>
        <p className="mt-1 text-sm text-gray-500">
          Here's what's happening at your organization today.
        </p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-5">
        <StatCard
          title="Total Employees"
          value={stats.totalEmployees}
          icon={UsersIcon}
          color="text-blue-600"
          change="+2 this month"
        />
        <StatCard
          title="Departments"
          value={stats.totalDepartments}
          icon={BuildingOfficeIcon}
          color="text-green-600"
        />
        <StatCard
          title="Pending Leaves"
          value={stats.pendingLeaveRequests}
          icon={DocumentTextIcon}
          color="text-yellow-600"
        />
        <StatCard
          title="Today's Attendance"
          value={`${stats.todayAttendance}%`}
          icon={ClockIcon}
          color="text-purple-600"
        />
        <StatCard
          title="Monthly Payroll"
          value={`$${stats.monthlyPayroll.toLocaleString()}`}
          icon={CurrencyDollarIcon}
          color="text-red-600"
        />
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Attendance Chart */}
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Weekly Attendance</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={attendanceData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="present" fill="#10B981" name="Present" />
              <Bar dataKey="absent" fill="#EF4444" name="Absent" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Department Distribution */}
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Employee Distribution by Department</h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={departmentData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
              >
                {departmentData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Recent Activity */}
      <div className="bg-white shadow rounded-lg">
        <div className="px-4 py-5 sm:p-6">
          <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">
            Recent Activity
          </h3>
          <div className="space-y-3">
            <div className="flex items-center space-x-3">
              <div className="flex-shrink-0">
                <div className="h-2 w-2 bg-green-400 rounded-full"></div>
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-sm text-gray-900">
                  John Doe submitted a leave request for next week
                </p>
                <p className="text-sm text-gray-500">2 hours ago</p>
              </div>
            </div>
            <div className="flex items-center space-x-3">
              <div className="flex-shrink-0">
                <div className="h-2 w-2 bg-blue-400 rounded-full"></div>
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-sm text-gray-900">
                  New employee Sarah Johnson added to Engineering department
                </p>
                <p className="text-sm text-gray-500">4 hours ago</p>
              </div>
            </div>
            <div className="flex items-center space-x-3">
              <div className="flex-shrink-0">
                <div className="h-2 w-2 bg-yellow-400 rounded-full"></div>
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-sm text-gray-900">
                  Payroll for March has been processed
                </p>
                <p className="text-sm text-gray-500">1 day ago</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}