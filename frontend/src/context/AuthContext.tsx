'use client';

import React, { createContext, useState, useContext, useEffect, ReactNode } from 'react';
import { useRouter } from 'next/navigation';
import { jwtDecode } from 'jwt-decode';

export interface AuthContextType {

  user: { role: string; id: string; email: string } | null;
  login: (token: string) => void;
  logout: () => void;
  isAuthenticated: boolean;
  accessToken: string | null;
  hasRole: (roles: string[]) => boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [user, setUser] = useState<{ role: string; id: string; email: string } | null>(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [accessToken, setAccessToken] = useState<string | null>(null);
  const router = useRouter();

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    const userRole = localStorage.getItem('user_role');
    const userId = localStorage.getItem('user_id');
    const userEmail = localStorage.getItem('user_email');

    if (token && userRole && userId && userEmail) {
      try {
        const decodedToken: { exp: number } = jwtDecode(token);
        if (decodedToken.exp * 1000 > Date.now()) {
          setUser({ role: userRole, id: userId, email: userEmail });
          setIsAuthenticated(true);
          setAccessToken(token);
        } else {
          // Token expired
          logout();
        }
      } catch (error) {
        console.error('Failed to decode token:', error);
        logout();
      }
    } else {
      setIsAuthenticated(false);
      setUser(null);
      setAccessToken(null);
    }
  }, []);

  const login = (token: string) => {
    localStorage.setItem('access_token', token);
    const decodedToken: { role: string; sub: string; email: string } = jwtDecode(token);
    localStorage.setItem('user_role', decodedToken.role);
    localStorage.setItem('user_id', decodedToken.sub);
    localStorage.setItem('user_email', decodedToken.email);
    setUser({ role: decodedToken.role, id: decodedToken.sub, email: decodedToken.email });
    setIsAuthenticated(true);
    setAccessToken(token);
  };

  const logout = () => {
    localStorage.clear();
    setUser(null);
    setIsAuthenticated(false);
    setAccessToken(null);
    router.push('/login');
  };

  const hasRole = (roles: string[]) => {
    if (!user) return false;
    return roles.includes(user.role);
  };

  return (
    <AuthContext.Provider value={{ user, login, logout, isAuthenticated, accessToken, hasRole }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};