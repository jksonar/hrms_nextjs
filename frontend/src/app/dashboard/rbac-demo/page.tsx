'use client';

import { useAuth } from '@/contexts/AuthContext';
import { usePermissions } from '@/hooks/usePermissions';
import { ProtectedComponent, AdminOnly, HROnly, ManagerAndAbove } from '@/components/ProtectedComponent';
import { Permission } from '@/types/permissions';
import { UserRole } from '@/types';

export default function RBACDemoPage() {
  const { user } = useAuth();
  const { hasPermission, hasAnyPermission, userRole } = usePermissions();

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold text-gray-900 mb-6">RBAC Demo Page</h1>
      
      {/* User Info */}
      <div className="bg-white shadow rounded-lg p-6 mb-6">
        <h2 className="text-xl font-semibold mb-4">Current User Information</h2>
        <div className="grid grid-cols-2 gap-4">
          <div>
            <p className="text-sm font-medium text-gray-500">Name</p>
            <p className="text-lg">{user?.full_name || 'N/A'}</p>
          </div>
          <div>
            <p className="text-sm font-medium text-gray-500">Email</p>
            <p className="text-lg">{user?.email || 'N/A'}</p>
          </div>
          <div>
            <p className="text-sm font-medium text-gray-500">Role</p>
            <p className="text-lg capitalize">{user?.role || 'N/A'}</p>
          </div>
          <div>
            <p className="text-sm font-medium text-gray-500">User ID</p>
            <p className="text-lg">{user?.id || 'N/A'}</p>
          </div>
        </div>
      </div>

      {/* Role-Based Components Demo */}
      <div className="bg-white shadow rounded-lg p-6 mb-6">
        <h2 className="text-xl font-semibold mb-4">Role-Based Component Visibility</h2>
        
        <div className="space-y-4">
          <AdminOnly>
            <div className="bg-red-50 border border-red-200 rounded-md p-4">
              <h3 className="text-lg font-medium text-red-800">Admin Only Content</h3>
              <p className="text-red-700">This content is only visible to administrators.</p>
            </div>
          </AdminOnly>

          <HROnly>
            <div className="bg-blue-50 border border-blue-200 rounded-md p-4">
              <h3 className="text-lg font-medium text-blue-800">HR & Admin Content</h3>
              <p className="text-blue-700">This content is visible to HR staff and administrators.</p>
            </div>
          </HROnly>

          <ManagerAndAbove>
            <div className="bg-green-50 border border-green-200 rounded-md p-4">
              <h3 className="text-lg font-medium text-green-800">Manager+ Content</h3>
              <p className="text-green-700">This content is visible to managers, HR, and administrators.</p>
            </div>
          </ManagerAndAbove>

          <ProtectedComponent roles={[UserRole.EMPLOYEE, UserRole.MANAGER, UserRole.HR, UserRole.ADMIN]}>
            <div className="bg-gray-50 border border-gray-200 rounded-md p-4">
              <h3 className="text-lg font-medium text-gray-800">All Users Content</h3>
              <p className="text-gray-700">This content is visible to all authenticated users.</p>
            </div>
          </ProtectedComponent>
        </div>
      </div>

      {/* Permission-Based Components Demo */}
      <div className="bg-white shadow rounded-lg p-6 mb-6">
        <h2 className="text-xl font-semibold mb-4">Permission-Based Component Visibility</h2>
        
        <div className="space-y-4">
          <ProtectedComponent permission={Permission.CREATE_EMPLOYEE}>
            <div className="bg-purple-50 border border-purple-200 rounded-md p-4">
              <h3 className="text-lg font-medium text-purple-800">Create Employee Permission</h3>
              <p className="text-purple-700">You have permission to create employees.</p>
            </div>
          </ProtectedComponent>

          <ProtectedComponent permission={Permission.READ_PAYROLL}>
            <div className="bg-yellow-50 border border-yellow-200 rounded-md p-4">
              <h3 className="text-lg font-medium text-yellow-800">View Payroll Permission</h3>
              <p className="text-yellow-700">You have permission to view payroll data.</p>
            </div>
          </ProtectedComponent>

          <ProtectedComponent permission={Permission.APPROVE_LEAVE_REQUEST}>
            <div className="bg-indigo-50 border border-indigo-200 rounded-md p-4">
              <h3 className="text-lg font-medium text-indigo-800">Approve Leave Permission</h3>
              <p className="text-indigo-700">You have permission to approve leave requests.</p>
            </div>
          </ProtectedComponent>

          <ProtectedComponent 
            permissions={[Permission.ACCESS_SETTINGS, Permission.MANAGE_ROLES]} 
            requireAll={true}
            fallback={
              <div className="bg-red-50 border border-red-200 rounded-md p-4">
                <h3 className="text-lg font-medium text-red-800">Insufficient Permissions</h3>
                <p className="text-red-700">You need both settings access and role management permissions to see this content.</p>
              </div>
            }
          >
            <div className="bg-emerald-50 border border-emerald-200 rounded-md p-4">
              <h3 className="text-lg font-medium text-emerald-800">Advanced Admin Features</h3>
              <p className="text-emerald-700">You have full administrative permissions.</p>
            </div>
          </ProtectedComponent>
        </div>
      </div>

      {/* Permission Check Results */}
      <div className="bg-white shadow rounded-lg p-6">
        <h2 className="text-xl font-semibold mb-4">Permission Check Results</h2>
        
        <div className="grid grid-cols-2 gap-4">
          <div>
            <h3 className="font-medium mb-2">Employee Permissions</h3>
            <ul className="space-y-1 text-sm">
              <li className={hasPermission(Permission.CREATE_EMPLOYEE) ? 'text-green-600' : 'text-red-600'}>
                ✓ Create Employee: {hasPermission(Permission.CREATE_EMPLOYEE) ? 'Yes' : 'No'}
              </li>
              <li className={hasPermission(Permission.READ_EMPLOYEE) ? 'text-green-600' : 'text-red-600'}>
                ✓ Read Employee: {hasPermission(Permission.READ_EMPLOYEE) ? 'Yes' : 'No'}
              </li>
              <li className={hasPermission(Permission.UPDATE_EMPLOYEE) ? 'text-green-600' : 'text-red-600'}>
                ✓ Update Employee: {hasPermission(Permission.UPDATE_EMPLOYEE) ? 'Yes' : 'No'}
              </li>
              <li className={hasPermission(Permission.DELETE_EMPLOYEE) ? 'text-green-600' : 'text-red-600'}>
                ✓ Delete Employee: {hasPermission(Permission.DELETE_EMPLOYEE) ? 'Yes' : 'No'}
              </li>
            </ul>
          </div>
          
          <div>
            <h3 className="font-medium mb-2">System Permissions</h3>
            <ul className="space-y-1 text-sm">
              <li className={hasPermission(Permission.READ_PAYROLL) ? 'text-green-600' : 'text-red-600'}>
                ✓ View Payroll: {hasPermission(Permission.READ_PAYROLL) ? 'Yes' : 'No'}
              </li>
              <li className={hasPermission(Permission.APPROVE_LEAVE_REQUEST) ? 'text-green-600' : 'text-red-600'}>
                ✓ Approve Leave: {hasPermission(Permission.APPROVE_LEAVE_REQUEST) ? 'Yes' : 'No'}
              </li>
              <li className={hasPermission(Permission.ACCESS_REPORTS) ? 'text-green-600' : 'text-red-600'}>
                ✓ Access Reports: {hasPermission(Permission.ACCESS_REPORTS) ? 'Yes' : 'No'}
              </li>
              <li className={hasPermission(Permission.ACCESS_SETTINGS) ? 'text-green-600' : 'text-red-600'}>
                ✓ Access Settings: {hasPermission(Permission.ACCESS_SETTINGS) ? 'Yes' : 'No'}
              </li>
            </ul>
          </div>
        </div>
        
        <div className="mt-4 pt-4 border-t">
          <h3 className="font-medium mb-2">Complex Permission Checks</h3>
          <ul className="space-y-1 text-sm">
            <li className={hasAnyPermission([Permission.CREATE_EMPLOYEE, Permission.UPDATE_EMPLOYEE]) ? 'text-green-600' : 'text-red-600'}>
              ✓ Can manage employees (create OR update): {hasAnyPermission([Permission.CREATE_EMPLOYEE, Permission.UPDATE_EMPLOYEE]) ? 'Yes' : 'No'}
            </li>
            <li className={hasAnyPermission([Permission.APPROVE_LEAVE_REQUEST, Permission.REJECT_LEAVE_REQUEST]) ? 'text-green-600' : 'text-red-600'}>
              ✓ Can process leave requests: {hasAnyPermission([Permission.APPROVE_LEAVE_REQUEST, Permission.REJECT_LEAVE_REQUEST]) ? 'Yes' : 'No'}
            </li>
          </ul>
        </div>
      </div>
    </div>
  );
}