import { useAuth } from '@/contexts/AuthContext';
import { Permission } from '@/types/permissions';
import { hasPermission, hasAnyPermission, hasAllPermissions } from '@/utils/permissions';

export const usePermissions = () => {
  const { user } = useAuth();
  
  const checkPermission = (permission: Permission): boolean => {
    return hasPermission(user?.role, permission);
  };
  
  const checkAnyPermission = (permissions: Permission[]): boolean => {
    return hasAnyPermission(user?.role, permissions);
  };
  
  const checkAllPermissions = (permissions: Permission[]): boolean => {
    return hasAllPermissions(user?.role, permissions);
  };
  
  return {
    hasPermission: checkPermission,
    hasAnyPermission: checkAnyPermission,
    hasAllPermissions: checkAllPermissions,
    userRole: user?.role,
  };
};