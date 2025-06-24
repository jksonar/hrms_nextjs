'use client';

import React, { createContext, useContext, useEffect, useState } from 'react';
import Cookies from 'js-cookie';
import { User, AuthResponse, LoginCredentials } from '@/types';
import { authAPI } from '@/lib/api';
import toast from 'react-hot-toast';

interface AuthContextType {
  user: User | null;
  loading: boolean;
  login: (credentials: LoginCredentials) => Promise<boolean>;
  logout: () => void;
  isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

interface AuthProviderProps {
  children: React.ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const initAuth = async () => {
      const token = Cookies.get('access_token');
      const userData = Cookies.get('user_data');
      
      if (token && userData) {
        try {
          const parsedUser = JSON.parse(userData);
          setUser(parsedUser);
        } catch (error) {
          console.error('Error parsing user data:', error);
          Cookies.remove('access_token');
          Cookies.remove('refresh_token');
          Cookies.remove('user_data');
        }
      }
      setLoading(false);
    };

    initAuth();
  }, []);

  const login = async (credentials: LoginCredentials): Promise<boolean> => {
    try {
      setLoading(true);
      const response = await authAPI.login(credentials);
      const authData: AuthResponse = response.data;
      
      // Store tokens
      Cookies.set('access_token', authData.access_token, { expires: 1 });
      Cookies.set('refresh_token', authData.refresh_token, { expires: 7 });
      
      // Decode user info from token (you might want to get this from a separate endpoint)
      // For now, we'll make a request to get user info
      try {
        // You might need to create a /me endpoint in your backend
        // For now, we'll store basic user info
        const userData = {
          id: 1, // This should come from token or separate API call
          email: credentials.email,
          full_name: 'User', // This should come from API
          role: 'employee' as any, // This should come from token
          is_active: true,
          created_at: new Date().toISOString(),
          updated_at: new Date().toISOString(),
        };
        
        setUser(userData);
        Cookies.set('user_data', JSON.stringify(userData), { expires: 1 });
        
        toast.success('Login successful!');
        return true;
      } catch (userError) {
        console.error('Error fetching user data:', userError);
        return false;
      }
    } catch (error: any) {
      console.error('Login error:', error);
      toast.error(error.response?.data?.detail || 'Login failed');
      return false;
    } finally {
      setLoading(false);
    }
  };

  const logout = () => {
    authAPI.logout();
    setUser(null);
    Cookies.remove('user_data');
    toast.success('Logged out successfully');
  };

  const value: AuthContextType = {
    user,
    loading,
    login,
    logout,
    isAuthenticated: !!user,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};