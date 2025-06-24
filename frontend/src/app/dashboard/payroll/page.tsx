'use client';

import { useState, useEffect } from 'react';
import { DocumentArrowDownIcon, CurrencyDollarIcon, CalendarIcon } from '@heroicons/react/24/outline';
import { payrollAPI, employeesAPI } from '@/lib/api';
import { Payroll, Employee } from '@/types';
import { useAuth } from '@/contexts/AuthContext';
import toast from 'react-hot-toast';
import { format } from 'date-fns';

export default function PayrollPage() {
  const { user } = useAuth();
  const [payrollRecords, setPayrollRecords] = useState<Payroll[]>([]);
  const [employees, setEmployees] = useState<Employee[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedEmployee, setSelectedEmployee] = useState<number | null>(null);
  const [selectedMonth, setSelectedMonth] = useState(format(new Date(), 'yyyy-MM'));
  const [generatingPayslip, setGeneratingPayslip] = useState<number | null>(null);

  useEffect(() => {
    fetchData();
  }, [user]);

  useEffect(() => {
    fetchPayrollRecords();
  }, [selectedEmployee, selectedMonth, user]);

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

  const fetchPayrollRecords = async () => {
    try {
      let response;
      if (user?.role === 'employee') {
        response = await payrollAPI.getByEmployee(user.id);
      } else if (selectedEmployee) {
        response = await payrollAPI.getByEmployee(selectedEmployee);
      } else {
        response = await payrollAPI.getAll();
      }
      
      // Filter by selected month if specified
      let filteredRecords = response.data;
      if (selectedMonth) {
        filteredRecords = filteredRecords.filter((record: Payroll) => {
          const recordMonth = format(new Date(record.pay_period_start), 'yyyy-MM');
          return recordMonth === selectedMonth;
        });
      }
      
      setPayrollRecords(filteredRecords);
    } catch (error) {
      toast.error('Failed to fetch payroll records');
    }
  };

  const handleGeneratePayslip = async (payrollId: number) => {
    setGeneratingPayslip(payrollId);
    try {
      const response = await payrollAPI.generatePayslip(payrollId);
      
      // Create a blob from the response and download it
      const blob = new Blob([response.data], { type: 'application/pdf' });
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `payslip-${payrollId}.pdf`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
      
      toast.success('Payslip downloaded successfully');
    } catch (error) {
      toast.error('Failed to generate payslip');
    } finally {
      setGeneratingPayslip(null);
    }
  };

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
    }).format(amount);
  };

  const calculateNetPay = (record: Payroll) => {
    return record.basic_salary + (record.allowances || 0) - (record.deductions || 0);
  };

  const canViewAllPayroll = user?.role === 'admin' || user?.role === 'hr';

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
        <h1 className="text-2xl font-bold text-gray-900">Payroll</h1>
        <div className="flex items-center gap-2 text-sm text-gray-500">
          <CurrencyDollarIcon className="h-5 w-5" />
          Payroll Management
        </div>
      </div>

      {/* Summary Cards */}
      {canViewAllPayroll && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-white overflow-hidden shadow rounded-lg">
            <div className="p-5">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <CurrencyDollarIcon className="h-8 w-8 text-gray-400" />
                </div>
                <div className="ml-5 w-0 flex-1">
                  <dl>
                    <dt className="text-sm font-medium text-gray-500 truncate">
                      Total Payroll This Month
                    </dt>
                    <dd className="text-lg font-medium text-gray-900">
                      {formatCurrency(
                        payrollRecords.reduce((sum, record) => sum + calculateNetPay(record), 0)
                      )}
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>
          
          <div className="bg-white overflow-hidden shadow rounded-lg">
            <div className="p-5">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <CalendarIcon className="h-8 w-8 text-gray-400" />
                </div>
                <div className="ml-5 w-0 flex-1">
                  <dl>
                    <dt className="text-sm font-medium text-gray-500 truncate">
                      Employees Paid
                    </dt>
                    <dd className="text-lg font-medium text-gray-900">
                      {payrollRecords.length}
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>
          
          <div className="bg-white overflow-hidden shadow rounded-lg">
            <div className="p-5">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <DocumentArrowDownIcon className="h-8 w-8 text-gray-400" />
                </div>
                <div className="ml-5 w-0 flex-1">
                  <dl>
                    <dt className="text-sm font-medium text-gray-500 truncate">
                      Average Salary
                    </dt>
                    <dd className="text-lg font-medium text-gray-900">
                      {payrollRecords.length > 0
                        ? formatCurrency(
                            payrollRecords.reduce((sum, record) => sum + calculateNetPay(record), 0) /
                              payrollRecords.length
                          )
                        : '$0'}
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Filters */}
      <div className="bg-white shadow rounded-lg p-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Month
            </label>
            <input
              type="month"
              value={selectedMonth}
              onChange={(e) => setSelectedMonth(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
            />
          </div>
          {canViewAllPayroll && (
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

      {/* Payroll Records */}
      <div className="bg-white shadow rounded-lg">
        <div className="px-6 py-4 border-b border-gray-200">
          <h2 className="text-lg font-medium text-gray-900">Payroll Records</h2>
        </div>
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                {canViewAllPayroll && (
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Employee
                  </th>
                )}
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Pay Period
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Basic Salary
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Allowances
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Deductions
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Net Pay
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Status
                </th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Actions
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {payrollRecords.map((record) => (
                <tr key={record.id} className="hover:bg-gray-50">
                  {canViewAllPayroll && (
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                      {record.employee?.first_name} {record.employee?.last_name}
                    </td>
                  )}
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    <div>
                      <div>{format(new Date(record.pay_period_start), 'MMM d')}</div>
                      <div className="text-xs text-gray-400">
                        to {format(new Date(record.pay_period_end), 'MMM d, yyyy')}
                      </div>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {formatCurrency(record.basic_salary)}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {formatCurrency(record.allowances || 0)}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {formatCurrency(record.deductions || 0)}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                    {formatCurrency(calculateNetPay(record))}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className="px-2 py-1 text-xs font-medium rounded-full bg-green-100 text-green-800">
                      Paid
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                    <button
                      onClick={() => handleGeneratePayslip(record.id)}
                      disabled={generatingPayslip === record.id}
                      className="text-indigo-600 hover:text-indigo-900 flex items-center gap-1 ml-auto disabled:opacity-50"
                    >
                      <DocumentArrowDownIcon className="h-4 w-4" />
                      {generatingPayslip === record.id ? 'Generating...' : 'Download'}
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {payrollRecords.length === 0 && (
          <div className="text-center py-12">
            <CurrencyDollarIcon className="mx-auto h-12 w-12 text-gray-400" />
            <p className="mt-2 text-gray-500">No payroll records found for the selected period.</p>
          </div>
        )}
      </div>

      {/* Payroll Summary */}
      {user?.role === 'employee' && payrollRecords.length > 0 && (
        <div className="bg-white shadow rounded-lg p-6">
          <h2 className="text-lg font-medium text-gray-900 mb-4">Your Payroll Summary</h2>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div className="text-center">
              <div className="text-2xl font-bold text-gray-900">
                {formatCurrency(
                  payrollRecords.reduce((sum, record) => sum + record.basic_salary, 0) /
                    payrollRecords.length
                )}
              </div>
              <div className="text-sm text-gray-500">Average Basic Salary</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-green-600">
                {formatCurrency(
                  payrollRecords.reduce((sum, record) => sum + (record.allowances || 0), 0)
                )}
              </div>
              <div className="text-sm text-gray-500">Total Allowances</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-red-600">
                {formatCurrency(
                  payrollRecords.reduce((sum, record) => sum + (record.deductions || 0), 0)
                )}
              </div>
              <div className="text-sm text-gray-500">Total Deductions</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-indigo-600">
                {formatCurrency(
                  payrollRecords.reduce((sum, record) => sum + calculateNetPay(record), 0)
                )}
              </div>
              <div className="text-sm text-gray-500">Total Net Pay</div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}