'use client';

import { redirect } from 'next/navigation';

// This is a placeholder for actual role-based logic.
// In a real application, you would fetch the user's role from an authentication context or API.
const getUserRole = () => {
  // For demonstration purposes, let's assume a default role or fetch from a mock API/context
  // Possible roles: 'employee', 'manager', 'hr', 'admin'
  // You would replace this with actual authentication and role management logic
  return 'employee'; // Defaulting to employee for now
};

const DashboardPage = () => {
  const userRole = getUserRole();

  switch (userRole) {
    case 'employee':
      redirect('/dashboard/employee');
      break;
    case 'manager':
      redirect('/dashboard/manager');
      break;
    case 'hr':
      redirect('/dashboard/hr');
      break;
    case 'admin':
      redirect('/dashboard/admin');
      break;
    default:
      redirect('/login'); // Redirect to login if role is not recognized
  }

  return null; // Will not render anything as it redirects
};

export default DashboardPage;