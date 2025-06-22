'use client';

import DashboardLayout from '@/components/DashboardLayout';
import { useState, useEffect } from 'react';
import { useAuth } from '@/context/AuthContext';

interface User {
  id: number;
  email: string;
  role: string;
}

export default function UsersPage() {
  const { user, isAuthenticated, accessToken }: { user: any, isAuthenticated: boolean, accessToken: string | null } = useAuth();
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!isAuthenticated || !accessToken) {
      setLoading(false);
      setError('User not authenticated or access token not available.');
      return;
    }

    const fetchUsers = async () => {
      try {
        const response = await fetch('http://localhost:8000/api/v1/users', {
          headers: {
            'Authorization': `Bearer ${accessToken}`,
          },
        });

        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.detail || 'Failed to fetch users');
        }

        const data: User[] = await response.json();
        setUsers(data);
      } catch (err: any) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchUsers();
  }, [isAuthenticated, accessToken]);

  if (loading) {
    return (
      <DashboardLayout>
        <h1 className="text-2xl font-bold">Users</h1>
        <p>Loading users...</p>
      </DashboardLayout>
    );
  }

  if (error) {
    return (
      <DashboardLayout>
        <h1 className="text-2xl font-bold">Users</h1>
        <p className="text-red-500">Error: {error}</p>
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout>
      <h1 className="text-2xl font-bold">Users</h1>
      <p>Manage user accounts and roles.</p>
      <div className="mt-8">
        {users.length === 0 ? (
          <p>No users found.</p>
        ) : (
          <table className="min-w-full bg-white border border-gray-200">
            <thead>
              <tr>
                <th className="py-2 px-4 border-b">ID</th>
                <th className="py-2 px-4 border-b">Email</th>
                <th className="py-2 px-4 border-b">Role</th>
              </tr>
            </thead>
            <tbody>
              {users.map((user) => (
                <tr key={user.id}>
                  <td className="py-2 px-4 border-b text-center">{user.id}</td>
                  <td className="py-2 px-4 border-b text-center">{user.email}</td>
                  <td className="py-2 px-4 border-b text-center">{user.role}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </DashboardLayout>
  );
}