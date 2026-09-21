import React, { createContext, useContext, useState, useEffect } from 'react';
import { User, UserProfile } from '../types';
import { authApi, usersApi } from '../services/api';

interface AuthContextType {
  user: UserProfile | User | null;
  token: string | null;
  isAuthenticated: boolean;
  isAdmin: boolean;
  loading: boolean;
  login: (token: string, userData: User) => void;
  logout: () => void;
  refreshProfile: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<UserProfile | User | null>(null);
  const [token, setToken] = useState<string | null>(localStorage.getItem('skillswap_token'));
  const [loading, setLoading] = useState<boolean>(true);

  const refreshProfile = async () => {
    try {
      if (token) {
        const res = await usersApi.getProfile();
        setUser(res.data);
        localStorage.setItem('skillswap_user', JSON.stringify(res.data));
      }
    } catch (err) {
      console.error('Failed to fetch profile:', err);
    }
  };

  useEffect(() => {
    const initAuth = async () => {
      const savedToken = localStorage.getItem('skillswap_token');
      const savedUser = localStorage.getItem('skillswap_user');

      if (savedToken) {
        setToken(savedToken);
        if (savedUser) {
          try {
            setUser(JSON.parse(savedUser));
          } catch (e) {
            // ignore
          }
        }
        try {
          const res = await usersApi.getProfile();
          setUser(res.data);
          localStorage.setItem('skillswap_user', JSON.stringify(res.data));
        } catch (e) {
          console.warn('Token expired or invalid');
          localStorage.removeItem('skillswap_token');
          localStorage.removeItem('skillswap_user');
          setToken(null);
          setUser(null);
        }
      }
      setLoading(false);
    };

    initAuth();
  }, []);

  const login = (newToken: string, userData: User) => {
    localStorage.setItem('skillswap_token', newToken);
    localStorage.setItem('skillswap_user', JSON.stringify(userData));
    setToken(newToken);
    setUser(userData);
    refreshProfile();
  };

  const logout = () => {
    localStorage.removeItem('skillswap_token');
    localStorage.removeItem('skillswap_user');
    setToken(null);
    setUser(null);
  };

  const isAuthenticated = !!token && !!user;
  const isAdmin = user?.role === 'admin';

  return (
    <AuthContext.Provider
      value={{
        user,
        token,
        isAuthenticated,
        isAdmin,
        loading,
        login,
        logout,
        refreshProfile,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
