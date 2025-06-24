'use client';

import { useState, useEffect } from 'react';
import { ClockIcon, CalendarIcon } from '@heroicons/react/24/outline';
import { attendanceAPI, employeesAPI } from '@/lib/api';
import { Attendance, Employee, AttendanceStatus } from '@/types';
import { useAuth } from '@/contexts/AuthContext';
import toast from 'react-hot-toast';
import { format } from 'date-fns';

export default function AttendancePage() {
  const { user } = useAuth();
  const [attendanceRecords, setAttendanceRecords] = useState<Attendance[]>([]);
  const [employees, setEmployees] = useState<Employee[]>([]);
  const [loading, setLoading] = useState(true);
  const [clockingIn, setClocingIn] = useState(false);
  const [clockingOut, setClocingOut] = useState(false);
  const [selectedDate, setSelectedDate] = useState(format(new Date(), 'yyyy-MM-dd'));
  const [selectedEmployee, setSelectedEmployee] = useState<number | null>(null);
  const [todayAttendance, setTodayAttendance] = useState<Attendance | null>(null);

  useEffect(() => {
    fetchData();
    if (user?.role === 'employee') {
      fetchTodayAttendance();
    }
  }, [user]);

  useEffect(() => {
    fetchAttendanceRecords();
  }, [selectedDate, selectedEmployee]);

  const fetchData = async () => {
    try {
      if (user?.role === 'admin' || user?.role === 'hr') {
        const employeesResponse = await employeesAPI.getAll();
        setEmployees(employeesResponse.data);
      }
    } catch (error) {
      toast.error('Failed to fetch data');
    } finally {
      setLoading(false);
    }
  };

  const fetchTodayAttendance = async () => {
    try {
      const today = format(new Date(), 'yyyy-MM-dd');
      const response = await attendanceAPI.getByEmployee(user!.id, today, today);
      if (response.data.length > 0) {
        setTodayAttendance(response.data[0]);
      }
    } catch (error) {
      console.error('Failed to fetch today attendance');
    }
  };

  const fetchAttendanceRecords = async () => {
    try {
      let response;
      if (user?.role === 'employee') {
        response = await attendanceAPI.getByEmployee(user.id, selectedDate, selectedDate);
      } else if (selectedEmployee) {
        response = await attendanceAPI.getByEmployee(selectedEmployee, selectedDate, selectedDate);
      } else {
        response = await attendanceAPI.getAll();
      }
      setAttendanceRecords(response.data);
    } catch (error) {
      toast.error('Failed to fetch attendance records');
    }
  };

  const handleClockIn = async () => {
    setClocingIn(true);
    try {
      await attendanceAPI.clockIn(user?.id);
      toast.success('Clocked in successfully');
      await fetchTodayAttendance();
      await fetchAttendanceRecords();
    } catch (error) {
      toast.error('Failed to clock in');
    } finally {
      setClocingIn(false);
    }
  };

  const handleClockOut = async () => {
    setClocingOut(true);
    try {
      if (todayAttendance) {
        await attendanceAPI.clockOut(todayAttendance.id);
        toast.success('Clocked out successfully');
        await fetchTodayAttendance();
        await fetchAttendanceRecords();
      }
    } catch (error) {
      toast.error('Failed to clock out');
    } finally {
      setClocingOut(false);
    }
  };

  const getStatusBadge = (status: AttendanceStatus) => {
    const statusColors: Record<string, string> = {
      present: 'bg-green-100 text-green-800',
      absent: 'bg-red-100 text-red-800',
      late: 'bg-yellow-100 text-yellow-800',
      half_day: 'bg-blue-100 text-blue-800',
    };

    return (
      <span className={`px-2 py-1 text-xs font-medium rounded-full ${statusColors[status] || 'bg-gray-100 text-gray-800'}`}>
        {status}
      </span>
    );
  };

  const formatTime = (timeString: string | null) => {
    if (!timeString) return '-';
    return format(new Date(`2000-01-01T${timeString}`), 'HH:mm');
  };

  const calculateHours = (clockIn: string | null, clockOut: string | null) => {
    if (!clockIn || !clockOut) return '-';
    
    const start = new Date(`2000-01-01T${clockIn}`);
    const end = new Date(`2000-01-01T${clockOut}`);
    const diff = (end.getTime() - start.getTime()) / (1000 * 60 * 60);
    
    return `${diff.toFixed(1)}h`;
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold text-gray-900">Attendance</h1>
        <div className="text-sm text-gray-500">
          {format(new Date(), 'EEEE, MMMM d, yyyy')}
        </div>
      </div>

      {/* Clock In/Out Section for Employees */}
      {user?.role === 'employee' && (
        <div className="bg-white shadow rounded-lg p-6">
          <h2 className="text-lg font-medium text-gray-900 mb-4">Today's Attendance</h2>
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <ClockIcon className="h-8 w-8 text-gray-400" />
              <div>
                <p className="text-sm text-gray-500">Current Status</p>
                <p className="text-lg font-medium">
                  {todayAttendance ? (
                    todayAttendance.clock_out_time ? 'Clocked Out' : 'Clocked In'
                  ) : (
                    'Not Clocked In'
                  )}
                </p>
              </div>
            </div>
            <div className="flex gap-3">
              {!todayAttendance ? (
                <button
                  onClick={handleClockIn}
                  disabled={clockingIn}
                  className="bg-green-600 text-white px-4 py-2 rounded-md hover:bg-green-700 disabled:opacity-50 flex items-center gap-2"
                >
                  <ClockIcon className="h-5 w-5" />
                  {clockingIn ? 'Clocking In...' : 'Clock In'}
                </button>
              ) : (
                !todayAttendance.clock_out_time && (
                  <button
                    onClick={handleClockOut}
                    disabled={clockingOut}
                    className="bg-red-600 text-white px-4 py-2 rounded-md hover:bg-red-700 disabled:opacity-50 flex items-center gap-2"
                  >
                    <ClockIcon className="h-5 w-5" />
                    {clockingOut ? 'Clocking Out...' : 'Clock Out'}
                  </button>
                )
              )}
            </div>
          </div>
          {todayAttendance && (
            <div className="mt-4 grid grid-cols-3 gap-4 text-sm">
              <div>
                <p className="text-gray-500">Clock In</p>
                <p className="font-medium">{formatTime(todayAttendance.clock_in_time)}</p>
              </div>
              <div>
                <p className="text-gray-500">Clock Out</p>
                <p className="font-medium">{formatTime(todayAttendance.clock_out_time ?? null)}</p>
              </div>
              <div>
                <p className="text-gray-500">Hours Worked</p>
                <p className="font-medium">
                  {calculateHours(todayAttendance.clock_in_time, todayAttendance.clock_out_time ?? null)}
                </p>
              </div>
            </div>
          )}
        </div>
      )}

      {/* Filters */}
      <div className="bg-white shadow rounded-lg p-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Date
            </label>
            <input
              type="date"
              value={selectedDate}
              onChange={(e) => setSelectedDate(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
            />
          </div>
          {(user?.role === 'admin' || user?.role === 'hr') && (
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Employee
              </label>
              <select
                value={selectedEmployee || ''}
                onChange={(e) => setSelectedEmployee(e.target.value ? Number(e.target.value) : null)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
              >
                <option value="">All Employees</option>
                {employees.map((employee) => (
                  <option key={employee.id} value={employee.id}>
                    {employee.first_name} {employee.last_name}
                  </option>
                ))}
              </select>
            </div>
          )}
        </div>
      </div>

      {/* Attendance Records */}
      <div className="bg-white shadow rounded-lg">
        <div className="px-6 py-4 border-b border-gray-200">
          <h2 className="text-lg font-medium text-gray-900">Attendance Records</h2>
        </div>
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                {(user?.role === 'admin' || user?.role === 'hr') && (
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Employee
                  </th>
                )}
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Date
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Clock In
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Clock Out
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Hours
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Status
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {attendanceRecords.map((record) => (
                <tr key={record.id} className="hover:bg-gray-50">
                  {(user?.role === 'admin' || user?.role === 'hr') && (
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                      {record.employee?.first_name} {record.employee?.last_name}
                    </td>
                  )}
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {format(new Date(record.date), 'MMM d, yyyy')}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {formatTime(record.clock_in_time)}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {formatTime(record.clock_out_time ?? null)}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {calculateHours(record.clock_in_time ?? null, record.clock_out_time ?? null)}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    {getStatusBadge(record.status)}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {attendanceRecords.length === 0 && (
          <div className="text-center py-12">
            <CalendarIcon className="mx-auto h-12 w-12 text-gray-400" />
            <p className="mt-2 text-gray-500">No attendance records found for the selected date.</p>
          </div>
        )}
      </div>
    </div>
  );
}