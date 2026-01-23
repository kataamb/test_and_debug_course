// src/TelegramProvider.jsx
import { useEffect } from 'react';
import WebApp from '@twa-dev/sdk';

const TelegramProvider = ({ children }) => {
  useEffect(() => {
    // Проверяем, что мы в Telegram Web App
    if (window.Telegram && window.Telegram.WebApp) {
      // Альтернативный способ инициализации
      window.Telegram.WebApp.ready();
      window.Telegram.WebApp.expand();
    }
    
    // Используем библиотеку @twa-dev/sdk
    if (WebApp.initDataUnsafe.user) {
      console.log('User:', WebApp.initDataUnsafe.user);
      
      // Основные настройки
      WebApp.expand(); // Раскрыть на весь экран
      WebApp.enableClosingConfirmation(); // Запрос подтверждения при закрытии
      
      // Дополнительные настройки (опционально)
      WebApp.setHeaderColor('#6D48E5'); // Цвет шапки
      WebApp.setBackgroundColor('#f0f0f0'); // Цвет фона
      WebApp.MainButton.setText('Сохранить'); // Текст кнопки
      WebApp.MainButton.show(); // Показать кнопку
      
      // Подписка на события
      WebApp.onEvent('viewportChanged', () => {
        console.log('Viewport changed');
      });
      
      WebApp.MainButton.onClick(() => {
        console.log('Main button clicked');
        // Ваша логика при нажатии
      });
    } else {
      console.log('Not in Telegram Web App. Running in browser mode.');
      // Можно показать альтернативный интерфейс для браузера
    }
  }, []);

  return children;
};

export default TelegramProvider;
