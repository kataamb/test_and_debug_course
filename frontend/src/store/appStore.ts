// src/store/formStore.ts
import { create } from 'zustand';
import { persist } from 'zustand/middleware';

// ТОЛЬКО для сохранения черновика формы
interface FormStore {
  savedLoginForm: {
    email: string;
    password: string;
  };
  // Просто сохраняет форму
  saveLoginForm: (form: { email: string; password: string }) => void;
  // Очищает сохраненную форму
  clearSavedLoginForm: () => void;
}

export const useFormStore = create<FormStore>()(
  persist(
    (set) => ({
      savedLoginForm: {
        email: '',
        password: '',
      },
      
      saveLoginForm: (form) => 
        set({ savedLoginForm: form }),
      
      clearSavedLoginForm: () => 
        set({ savedLoginForm: { email: '', password: '' } }),
    }),
    {
      name: 'login-form-storage',
    }
  )
);
