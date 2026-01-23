// src/components/Login/Login.viewModel.ts
import { useState, useEffect } from 'react';
import { useAuth } from '../../contexts/AuthContext';
import { useNavigate } from 'react-router-dom';
import { useFormStore } from '../../store/appStore';

export const useLoginViewModel = () => {
  const auth = useAuth();
  const navigate = useNavigate();
  
  // Для сохранения формы
  const { savedLoginForm, saveLoginForm, clearSavedLoginForm } = useFormStore();
  
  // Старый код, как у вас было
  const [form, setForm] = useState(savedLoginForm); // Загружаем сохраненную форму
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  // Автосохранение при изменении
  useEffect(() => {
    saveLoginForm(form);
  }, [form, saveLoginForm]);

  const handleChange = (field: 'email' | 'password', value: string) => {
    setForm(prev => ({ ...prev, [field]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    if (!form.email || !form.password) {
      setError('Все поля обязательны');
      setLoading(false);
      return;
    }

    try {
      // Ваш старый логин
      await auth.login(form);
      console.log('✅ Успешный вход!');
      
      // Очищаем сохраненную форму после успешного входа
      clearSavedLoginForm();
      setForm({ email: '', password: '' }); // Очищаем локально
      
      navigate('/');
    } catch (err: any) {
      setError(err.message || 'Ошибка входа');
      // Форма НЕ очищается при ошибке - пользователь может исправить
    } finally {
      setLoading(false);
    }
  };

  return { form, handleChange, handleSubmit, loading, error };
};
