import React, { createContext, useContext, useEffect } from 'react';
import { useAuth as useAuthHook } from '../api/client/hooks/useUsers';

interface AuthContextType {
  user: any | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
  login: (credentials: any) => Promise<any>;
  logout: () => Promise<void>;
  register: (userData: any) => Promise<any>;
  fetchCurrentUser: () => Promise<any>;
  getToken: () => string | null;
  clearAuth: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const auth = useAuthHook();

  // При монтировании загружаем профиль если есть токен
  useEffect(() => {
    if (auth.isAuthenticated && !auth.user) {
      auth.fetchCurrentUser().catch(() => {
        // Если не удалось загрузить профиль - очищаем токен
        auth.clearAuth();
      });
    }
  }, [auth.isAuthenticated]);

  return (
    <AuthContext.Provider value={auth}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
};