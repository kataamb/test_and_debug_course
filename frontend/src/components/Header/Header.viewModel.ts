import { useState, useCallback } from 'react';
import { useAuth } from '../../contexts/AuthContext';
import { useNavigate } from 'react-router-dom';

export const useHeaderViewModel = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const { user, isAuthenticated, isLoading, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = useCallback(async () => {
    try {
      await logout();
      navigate('/');
    } catch (error) {
      console.error('Logout failed:', error);
    }
  }, [logout, navigate]);

  const handleKeyPress = useCallback((e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && searchQuery.trim()) {
      // Просто навигация на страницу поиска
      navigate(`/search?q=${encodeURIComponent(searchQuery)}`);
    }
  }, [searchQuery, navigate]);

  const handleNavigateToCreate = useCallback(() => navigate('/create-advert'), [navigate]);
  const handleNavigateToProfile = useCallback(() => navigate('/adverts'), [navigate]);
  const handleNavigateToAdverts = useCallback(() => navigate('/adverts'), [navigate]);
  const handleNavigateToLogin = useCallback(() => {
    console.log('DEBUG: navigating to login page');
    navigate('/login');
  }, [navigate]);
  const handleNavigateToRegister = useCallback(() => navigate('/register'), [navigate]);

  return {
    searchQuery,
    setSearchQuery,
    user,
    isAuthenticated,
    isLoading,
    userDisplayName: user?.email?.split('@')[0] || 'Пользователь',
    handleLogout,
    handleKeyPress,
    handleNavigateToCreate,
    handleNavigateToProfile,
    handleNavigateToAdverts,
    handleNavigateToLogin,
    handleNavigateToRegister,
  };
};
