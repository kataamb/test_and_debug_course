import React, { useState, useEffect } from 'react';
// ИМПОРТИРУЕМ ИЗ ТВОЕГО api.ts (а не из adverts-api!)
import { advertsApi } from '../api';

const ConnectionTest: React.FC = () => {
  const [status, setStatus] = useState<'idle' | 'loading' | 'success' | 'error'>('idle');
  const [message, setMessage] = useState('');
  const [adverts, setAdverts] = useState<any[]>([]);

  const testConnection = async () => {
    setStatus('loading');
    setMessage('Подключаемся к бэкенду...');

    try {
      // ВОТ! Теперь advertsApi УЖЕ НАСТРОЕН с правильным адресом
      const response = await advertsApi.getAllAdvertsApiV1AdvertsGet();

      setStatus('success');
      setMessage(`✅ Подключение успешно! Получено ${response.data.items.length} объявлений`);
      setAdverts(response.data.items);

      console.log('Данные с бэкенда:', response.data);

    } catch (error: any) {
      setStatus('error');

      if (error.response) {
        // Сервер ответил с ошибкой
        setMessage(`❌ Ошибка ${error.response.status}: ${error.response.data?.detail || 'Неизвестная ошибка'}`);
        console.error('Ответ сервера:', error.response.data);
        console.error('Статус:', error.response.status);
      } else if (error.request) {
        // Запрос был сделан, но ответа нет
        setMessage('❌ Нет ответа от сервера. Проверьте:\n1. Запущен ли бэкенд\n2. Правильный ли URL (localhost:8000?)\n3. CORS настройки');
        console.error('Не удалось получить ответ:', error.request);
      } else {
        // Ошибка при настройке запроса
        setMessage(`❌ Ошибка: ${error.message}`);
        console.error('Ошибка:', error.message);
      }
    }
  };

  useEffect(() => {
    testConnection();
  }, []);

  // ... остальной код (рендер) оставь как у тебя было ...
  return (
    <div style={{
      padding: '20px',
      border: `2px solid ${status === 'success' ? 'green' : status === 'error' ? 'red' : 'gray'}`,
      borderRadius: '8px',
      margin: '20px',
      backgroundColor: '#f9f9f9'
    }}>
      <h3>Тест подключения к бэкенду</h3>

      <div style={{ marginBottom: '10px' }}>
        <strong>Адрес бэкенда:</strong> http://localhost:8000
      </div>

      <div style={{ marginBottom: '10px' }}>
        <strong>Статус:</strong>
        <span style={{
          color: status === 'success' ? 'green' :
                 status === 'error' ? 'red' :
                 status === 'loading' ? 'orange' : 'gray',
          fontWeight: 'bold',
          marginLeft: '10px'
        }}>
          {status === 'loading' ? '⏳ Загрузка...' :
           status === 'success' ? '✅ Успех' :
           status === 'error' ? '❌ Ошибка' : 'Ожидание'}
        </span>
      </div>

      <div style={{
        marginBottom: '20px',
        whiteSpace: 'pre-line',
        backgroundColor: '#fff',
        padding: '10px',
        borderRadius: '4px',
        border: '1px solid #ddd'
      }}>
        {message}
      </div>

      <button
        onClick={testConnection}
        disabled={status === 'loading'}
        style={{
          padding: '10px 20px',
          backgroundColor: status === 'success' ? '#4CAF50' : '#2196F3',
          color: 'white',
          border: 'none',
          borderRadius: '4px',
          cursor: status === 'loading' ? 'wait' : 'pointer',
          fontSize: '16px'
        }}
      >
        {status === 'loading' ? 'Проверяем...' : 'Проверить снова'}
      </button>

      {adverts.length > 0 && (
        <div style={{ marginTop: '20px' }}>
          <h4>Объявления с бэкенда:</h4>
          <div style={{
            maxHeight: '300px',
            overflowY: 'auto',
            border: '1px solid #ddd',
            borderRadius: '4px',
            padding: '10px'
          }}>
            {adverts.map(advert => (
              <div key={advert.id} style={{
                borderBottom: '1px solid #eee',
                padding: '10px 0',
                marginBottom: '10px'
              }}>
                <strong>{advert.content}</strong>
                <p>{advert.description}</p>
                <small>Цена: {advert.price} руб.</small>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default ConnectionTest;