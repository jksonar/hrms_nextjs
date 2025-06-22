'use client';

import DashboardLayout from "@/components/DashboardLayout";

export default function EmployeeDetailPage({ params }: { params: { id: string } }) {
  return (
    <DashboardLayout>
      <h1 className="text-2xl font-bold">Employee Detail for ID: {params.id}</h1>
      <p>View and manage details for a specific employee.</p>
    </DashboardLayout>
  );
}