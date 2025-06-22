import React from 'react';
 import Link from 'next/link';
import { ReactNode } from 'react';
import {
  FaTachometerAlt,
  FaUsers,
  FaUserFriends,
  FaBuilding,
  FaBriefcase,
  FaCalendarCheck,
  FaCalendarTimes,
  FaMoneyBillAlt,
  FaSignOutAlt,
} from 'react-icons/fa';
import { useAuth } from '../context/AuthContext';

interface DashboardLayoutProps {
  children: ReactNode;
}

const DashboardLayout: React.FC<DashboardLayoutProps> = ({ children }) => {
  const { user, logout } = useAuth();
  const userRole = user?.role || '';
  const navItems = [
    { name: 'Dashboard', href: `/dashboard/${userRole.toLowerCase()}`, roles: ['EMPLOYEE', 'MANAGER', 'HR', 'ADMIN'], icon: FaTachometerAlt },
    { name: 'Users', href: '/dashboard/users', roles: ['ADMIN'], icon: FaUsers },
    { name: 'Employees', href: '/dashboard/employees', roles: ['ADMIN', 'HR', 'MANAGER'], icon: FaUserFriends },
    { name: 'Departments', href: '/dashboard/departments', roles: ['ADMIN', 'HR', 'MANAGER'], icon: FaBuilding },
    { name: 'Positions', href: '/dashboard/positions', roles: ['ADMIN', 'HR', 'MANAGER'], icon: FaBriefcase },
    { name: 'Attendance', href: '/dashboard/attendance', roles: ['ADMIN', 'HR', 'MANAGER', 'EMPLOYEE'], icon: FaCalendarCheck },
    { name: 'Leave Requests', href: '/dashboard/leave-requests', roles: ['ADMIN', 'HR', 'MANAGER', 'EMPLOYEE'], icon: FaCalendarTimes },
    { name: 'Payroll', href: '/dashboard/payroll', roles: ['ADMIN', 'HR', 'MANAGER', 'EMPLOYEE'], icon: FaMoneyBillAlt },
  ];

  return (
    <div className="flex h-screen bg-gray-100">
      {/* Sidebar */}
      <aside className="w-64 bg-gray-800 text-white flex flex-col">
        <div className="p-4 text-2xl font-bold border-b border-gray-700">
          HRMS Dashboard
        </div>
        <nav className="flex-1 p-4 space-y-2">
          {navItems.map((item) => {
            if (item.roles.includes(userRole)) {
              return (
                <Link key={item.name} href={item.href} className="flex items-center py-2 px-4 rounded hover:bg-gray-700">
                  <item.icon className="mr-3" />
                  {item.name}
                </Link>
              );
            }
            return null;
          })}

        </nav>
        <div className="p-4 border-t border-gray-700">
          <button onClick={logout} className="w-full py-2 px-4 rounded bg-red-600 hover:bg-red-700 flex items-center justify-center">
            <FaSignOutAlt className="mr-2" />
            Logout
          </button>
        </div>
      </aside>

      {/* Main content */}
      <main className="flex-1 flex flex-col overflow-hidden">
        {/* Header */}
        <header className="flex items-center justify-between p-4 bg-white border-b shadow-sm">
          <h1 className="text-xl font-semibold capitalize">{userRole} Dashboard</h1>
          <div>
            {/* User profile/settings can go here */}
            <span>Welcome, {user?.email}!</span>
          </div>
        </header>

        {/* Page content */}
        <div className="flex-1 overflow-auto p-4">
          {children}
        </div>
      </main>
    </div>
  );
};

export default DashboardLayout;