'use client';

import React from 'react';
import { useParams } from 'next/navigation';

const EmployeeDetailPage = () => {
  const params = useParams();
  const { id } = params;

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <div className="p-8 bg-white rounded shadow-md w-full max-w-md text-center">
        <h1 className="text-2xl font-bold mb-6">Employee Detail for ID: {id}</h1>
        <p>This page will display details and allow CRUD operations for employee {id}.</p>
      </div>
    </div>
  );
};

export default EmployeeDetailPage;