// src/types/state.ts
export interface AppState {
  loginForm?: {
    email: string;
    password: string;
  };
  ui?: {
    darkMode: boolean;
    language: string;
  };
  // Добавьте другие части состояния по мере необходимости
}

// Конфигурация
export const STORAGE_KEYS = {
  APP_STATE: 'my_tg_app_state',
  USER_PREFERENCES: 'my_tg_app_prefs',
} as const;
