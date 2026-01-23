import { useState, useCallback, useEffect } from 'react';
import { UsersApi } from '../api/users-api';
import { Configuration } from '../configuration';
import type { UserLogin, UserRegister } from '../api/users-api';


const getApiInstance = () => {
  const token = localStorage.getItem('access_token');

  const configuration = new Configuration({
    basePath: '',
    accessToken: token || undefined,
  });

  return new UsersApi(configuration);
};

export const useAuth = () => {
  const [user, setUser] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [api] = useState(getApiInstance());

  // Проверка аутентификации
  const isAuthenticated = !!localStorage.getItem('access_token');

  // Загрузка профиля пользователя

  const fetchCurrentUser = useCallback(async () => {
    if (!isAuthenticated) return;

    setLoading(true);
    try {
      const response = await api.getCurrentUserProfileApiV1UsersMeGet();
      setUser(response.data);
      setError(null);
    } catch (err: any) {
      const message = err.response?.data?.detail || 'Ошибка загрузки профиля';
      setError(message);
      localStorage.removeItem('access_token'); // Удаляем невалидный токен
    } finally {
      setLoading(false);
    }
  }, [api, isAuthenticated]);

  // Автоматически загружаем профиль при монтировании
  useEffect(() => {
    if (isAuthenticated && !user) {
      fetchCurrentUser();
    }
  }, [isAuthenticated, user, fetchCurrentUser]);

  // Вход
  const login = useCallback(
    async (credentials: UserLogin) => {
      setLoading(true);
      setError(null);

      try {
        const response = await api.loginUserApiV1UsersLoginPost(credentials);
        const token = response.data.access_token;

        if (token) {
          localStorage.setItem('access_token', token);
          // Обновляем API с новым токеном
          api.configuration.accessToken = token;
          await fetchCurrentUser(); // Загружаем профиль
        }

        return response.data;
      } catch (err: any) {
        const message = err.response?.data?.detail || 'Ошибка входа';
        setError(message);
        throw err;
      } finally {
        setLoading(false);
      }
    },
    [api, fetchCurrentUser]
  );

  // Выход
  const logout = useCallback(async () => {
    setLoading(true);
    try {
      await api.logoutUserApiV1UsersLogoutPost();
    } catch (err) {
      console.error('Ошибка при выходе:', err);
    } finally {
      localStorage.removeItem('access_token');
      setUser(null);
      api.configuration.accessToken = undefined;
      setLoading(false);
    }
  }, [api]);

  // Регистрация
  const register = useCallback(
    async (userData: UserRegister) => {
      setLoading(true);
      setError(null);

      try {
        const response = await api.registerUserApiV1UsersRegisterPost(userData);
        return response.data;
      } catch (err: any) {
        const message = err.response?.data?.detail || 'Ошибка регистрации';
        setError(message);
        throw err;
      } finally {
        setLoading(false);
      }
    },
    [api]
  );

  return {
    user,
    loading,
    isLoading: loading, // для обратной совместимости
    error,
    isAuthenticated,
    login,
    logout,
    register,
    fetchCurrentUser,
    clearError: () => setError(null),
    getToken: () => localStorage.getItem('access_token'),
    clearAuth: () => {
      localStorage.removeItem('access_token');
      setUser(null);
      setError(null);
    },
  };
};
