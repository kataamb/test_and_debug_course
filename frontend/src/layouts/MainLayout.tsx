// src/layouts/MainLayout.tsx
import React from 'react';
import { Outlet } from 'react-router-dom';
import { Header } from '../components/Header/Header';
import { useAuth } from '../contexts/AuthContext';

export const MainLayout: React.FC = () => {
  const { isAuthenticated, user, loading } = useAuth();

  return (
    <div className="app">
      {/* Header всегда показывается */}
      <Header
        isAuthenticated={isAuthenticated}
        userEmail={user?.email}
        isLoading={loading}
      />

      {/* Контент ВСЕГДА показывается! */}
      <main style={{ padding: '20px' }}>
        <Outlet />
      </main>
    </div>
  );
};