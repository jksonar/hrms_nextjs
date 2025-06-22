'use client';

'use client';

import DashboardLayout from '@/components/DashboardLayout';
import { useAuth } from '@/context/AuthContext';

export default function DashboardHome() {
  const { user } = useAuth();
  const userRole = user?.role || 'Guest';

  return (
    <DashboardLayout>
      <h1 className="text-2xl font-bold">Welcome to the HRMS Dashboard!</h1>
      <p>Select an option from the sidebar to get started.</p>
    </DashboardLayout>
  );
}