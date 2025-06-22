'use client';

import DashboardLayout from '@/components/DashboardLayout';
import { useState, useEffect } from 'react';
import { useAuth } from '@/context/AuthContext';

interface Employee {
  id: number;
  user_id: number;
  first_name: string;
  last_name: string;
  date_of_birth: string;
  phone_number: string;
  address: string;
  position: string;
  department_id: number;
}

export default function EmployeesPage() {
  const { user, isAuthenticated, accessToken }: { user: any, isAuthenticated: boolean, accessToken: string | null } = useAuth();
  const [employees, setEmployees] = useState<Employee[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!isAuthenticated || !accessToken) {
      setLoading(false);
      setError('User not authenticated or access token not available.');
      return;
    }

    const fetchEmployees = async () => {
      try {
        const response = await fetch('http://localhost:8000/api/v1/employees', {
          headers: {
            'Authorization': `Bearer ${accessToken}`,
          },
        });

        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.detail || 'Failed to fetch employees');
        }

        const data: Employee[] = await response.json();
        setEmployees(data);
      } catch (err: any) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchEmployees();
  }, [isAuthenticated, accessToken]);

  if (loading) {
    return (
      <DashboardLayout>
        <h1 className="text-2xl font-bold">Employees</h1>
        <p>Loading employees...</p>
      </DashboardLayout>
    );
  }

  if (error) {
    return (
      <DashboardLayout>
        <h1 className="text-2xl font-bold">Employees</h1>
        <p className="text-red-500">Error: {error}</p>
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout>
      <h1 className="text-2xl font-bold">Employees</h1>
      <p>Manage employee information.</p>
      <div className="mt-8">
        {employees.length === 0 ? (
          <p>No employees found.</p>
        ) : (
          <table className="min-w-full bg-white border border-gray-200">
            <thead>
              <tr>
                <th className="py-2 px-4 border-b">ID</th>
                <th className="py-2 px-4 border-b">User ID</th>
                <th className="py-2 px-4 border-b">First Name</th>
                <th className="py-2 px-4 border-b">Last Name</th>
                <th className="py-2 px-4 border-b">Position</th>
              </tr>
            </thead>
            <tbody>
              {employees.map((employee) => (
                <tr key={employee.id}>
                  <td className="py-2 px-4 border-b text-center">{employee.id}</td>
                  <td className="py-2 px-4 border-b text-center">{employee.user_id}</td>
                  <td className="py-2 px-4 border-b text-center">{employee.first_name}</td>
                  <td className="py-2 px-4 border-b text-center">{employee.last_name}</td>
                  <td className="py-2 px-4 border-b text-center">{employee.position}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </DashboardLayout>
  );
}