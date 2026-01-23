import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import './index.css';
import App from './App.tsx';
import { AuthProvider } from './contexts/AuthContext';

import TelegramProvider from './telegram_integration/TelegramProvider';

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <TelegramProvider>
      <AuthProvider>

        <App />

      </AuthProvider>
    </TelegramProvider>
  </StrictMode>,
);
