import React from 'react';
import DashboardLayout from '@/components/DashboardLayout';

export default function EmployeesPage() {
  return (
    <DashboardLayout>
      <h1 className="text-2xl font-bold">Employees</h1>
      <p>Manage employee information.</p>
    </DashboardLayout>
  );
}