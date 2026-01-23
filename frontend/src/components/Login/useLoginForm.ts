// src/hooks/useLoginForm.ts
import { useCallback, useRef } from 'react';
import { useAppStore } from '../../../store/appStore';
import { debounce } from '../../../utils/debounce';

export const useLoginForm = () => {
  const {
    loginForm,
    updateLoginForm,
    clearLoginForm,
  } = useAppStore();

  // Дебаунс для автосохранения
  const autoSaveRef = useRef(
    debounce((updates: Partial<typeof loginForm>) => {
      updateLoginForm(updates);
    }, 500)
  );

  const handleChange = useCallback((field: keyof typeof loginForm, value: string) => {
    // Немедленное обновление UI
    const updates = { [field]: value };
    
    // Автосохранение с дебаунсом
    autoSaveRef.current(updates);
    
    return updates;
  }, []);

  const handleSubmit = useCallback(async (formData: typeof loginForm) => {
    // Ваша логика отправки формы
    console.log('Submitting:', formData);
    
    // После успешной отправки очищаем
    clearLoginForm();
    
    return true;
  }, [clearLoginForm]);

  return {
    form: loginForm,
    handleChange,
    handleSubmit,
    clearForm: clearLoginForm,
  };
};
