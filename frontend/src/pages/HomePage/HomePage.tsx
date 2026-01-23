import React from 'react';
import { Header } from '../../components/Header/Header';
import { AdCardSmall } from '../../components/AdCardSmall/AdCardSmall';
import { useHomePageViewModel } from './HomePage.viewModel';

export const HomePage: React.FC = () => {
  const {
    ads,
    loading,
    error,
    sortByPrice,
    sortByPriceAsc,
    sortByPriceDesc,
    clearSort,
    refreshAds
  } = useHomePageViewModel();

  if (loading) {
    return (
      <div style={{ textAlign: 'center', padding: '40px' }}>
        <div>Загрузка объявлений...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div>
        <div style={{ color: 'red', padding: '20px' }}>
          Ошибка загрузки объявлений: {error}
        </div>
        <button onClick={refreshAds}>Повторить попытку</button>
      </div>
    );
  }

  return (
    <>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
        <h1>Последние объявления</h1>
        
        {/* Кнопки сортировки */}
        <div style={{ display: 'flex', gap: '10px', alignItems: 'center' }}>
          <span style={{ fontSize: '14px', color: '#666' }}>Сортировка:</span>
          <button 
            onClick={sortByPriceAsc}
            disabled={sortByPrice === 'asc'}
            style={{
              padding: '6px 12px',
              fontSize: '14px',
              backgroundColor: sortByPrice === 'asc' ? '#1976d2' : '#f0f0f0',
              color: sortByPrice === 'asc' ? 'white' : '#333',
              border: '1px solid #ddd',
              borderRadius: '4px',
              cursor: sortByPrice === 'asc' ? 'default' : 'pointer'
            }}
            title="Сортировка через Web Worker"
          >
            Цена ↑
          </button>
          <button 
            onClick={sortByPriceDesc}
            disabled={sortByPrice === 'desc'}
            style={{
              padding: '6px 12px',
              fontSize: '14px',
              backgroundColor: sortByPrice === 'desc' ? '#1976d2' : '#f0f0f0',
              color: sortByPrice === 'desc' ? 'white' : '#333',
              border: '1px solid #ddd',
              borderRadius: '4px',
              cursor: sortByPrice === 'desc' ? 'default' : 'pointer'
            }}
            title="Сортировка через Web Worker"
          >
            Цена ↓
          </button>
          {sortByPrice && (
            <button 
              onClick={clearSort}
              style={{
                padding: '6px 12px',
                fontSize: '14px',
                backgroundColor: '#f0f0f0',
                color: '#333',
                border: '1px solid #ddd',
                borderRadius: '4px',
                cursor: 'pointer'
              }}
            >
              Сбросить
            </button>
          )}
        </div>
      </div>

      {/* Индикатор сортировки */}
      {sortByPrice && (
        <div style={{ 
          padding: '10px', 
          marginBottom: '20px', 
          backgroundColor: '#e3f2fd', 
          borderRadius: '4px',
          fontSize: '14px'
        }}>
          Сортировка по цене: {sortByPrice === 'asc' ? 'по возрастанию' : 'по убыванию'}
          {typeof Worker !== 'undefined' ? ' (используется Web Worker)' : ' (Web Worker не поддерживается)'}
        </div>
      )}

      {ads.length === 0 ? (
        <div style={{ padding: '20px', textAlign: 'center' }}>
          Нет объявлений
        </div>
      ) : (
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '20px' }}>
          {ads.map(ad => (
            <AdCardSmall
              key={ad.id}
              id={ad.id}
              content={ad.title} 
              price={ad.price}
              date_created={ad.date}  
            />
          ))}
        </div>
      )}
    </>
  );
};

export default HomePage;
