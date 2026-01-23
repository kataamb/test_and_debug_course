import React from 'react';
import { Link } from '../Link';
import { TextField } from '../TextField';
import { useHeaderViewModel } from './Header.viewModel';

export const Header: React.FC = () => {
  const {
    searchQuery,
    isAuthenticated,
    isLoading,
    userDisplayName,
    setSearchQuery,
    handleLogout,
    handleKeyPress,
    handleNavigateToCreate,
    handleNavigateToProfile,
    handleNavigateToAdverts,
    handleNavigateToLogin,
    handleNavigateToRegister,
  } = useHeaderViewModel();

  if (isLoading) {
    return (
      <header>
        <div>Загрузка...</div>
      </header>
    );
  }

  return (
    <header>
      <div>
        <Link to="/">Главная</Link>
        <Link to="/wasm_demo">Wasm Demo</Link>
        {isAuthenticated && (
          <>
            <Link to="/logout" onClick={handleLogout}>Logout</Link>
            <Link to="/profile" onClick={handleNavigateToProfile}>Мой профиль</Link>
          </>
        )}
      </div>

      <div>
        <TextField
          value={searchQuery}
          onChange={setSearchQuery}
          placeholder="Поиск объявлений..."
          onKeyPress={handleKeyPress}
        />
      </div>

      <div>
        {isAuthenticated ? (
          <>
            <div><span>{userDisplayName}</span></div>

          </>
        ) : (
          <>
            <Link to="/login" onClick={handleNavigateToLogin}>Войти</Link>
            <Link to="/register" onClick={handleNavigateToRegister}>Регистрация</Link>
          </>
        )}
      </div>
    </header>
  );
};
