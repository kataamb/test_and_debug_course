import { useState, useEffect, useRef } from 'react';
import { useAdverts } from '../../api/client/hooks/useAdverts';

// Тип для UI карточки
export interface DisplayAd {
  id: number;
  title: string;
  price: number;
  location: string;
  date: string;
}

// Создаем inline Web Worker для сортировки
const createSortWorker = () => {
  if (typeof Worker === 'undefined') return null;
  
  const workerCode = `
    self.onmessage = function(event) {
      const { ads, sortDirection } = event.data;
      
    
      const adsCopy = [...ads];
      
      if (sortDirection === 'asc') {
    
        adsCopy.sort((a, b) => a.price - b.price);
      } else if (sortDirection === 'desc') {
      
        adsCopy.sort((a, b) => b.price - a.price);
      }
      
      self.postMessage({ sortedAds: adsCopy });
    };
  `;
  
  const blob = new Blob([workerCode], { type: 'application/javascript' });
  return new Worker(URL.createObjectURL(blob));
};

export const useHomePageViewModel = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [sortByPrice, setSortByPrice] = useState<'asc' | 'desc' | null>(null);
  const [isSorting, setIsSorting] = useState(false);
  const workerRef = useRef<Worker | null>(null);

  // Используем хук API
  const {
    data: apiResponse,
    loading,
    error,
    fetchAdverts
  } = useAdverts();

  const [ads, setAds] = useState<DisplayAd[]>([]);
  const [sortedAds, setSortedAds] = useState<DisplayAd[]>([]);

  // Инициализируем Worker один раз
  useEffect(() => {
    if (typeof Worker !== 'undefined') {
      workerRef.current = createSortWorker();
    }
    
    return () => {
      if (workerRef.current) {
        workerRef.current.terminate();
      }
    };
  }, []);

  // Загружаем данные при монтировании
  useEffect(() => {
    fetchAdverts();
  }, [fetchAdverts]);

  useEffect(() => {
    if (apiResponse?.items) {
      const convertedAds = apiResponse.items.map((item: any) => ({
        id: item.id,
        title: item.content || 'Без названия',
        price: item.price || 0,
        location: item.location || 'Не указано',
        date: item.date_created ? formatDate(item.date_created) : 'Сегодня'
      }));
      setAds(convertedAds);
      setSortedAds(convertedAds); // Изначально без сортировки
    }
  }, [apiResponse]);

  // Эффект для сортировки при изменении sortByPrice
  useEffect(() => {
    if (!sortByPrice || ads.length === 0) {
      setSortedAds(ads);
      return;
    }

    setIsSorting(true);

    if (workerRef.current) {
      // Используем Web Worker для сортировки
      const worker = workerRef.current;
      
      worker.onmessage = (event) => {
        setSortedAds(event.data.sortedAds);
        setIsSorting(false);
      };
      
      worker.postMessage({ 
        ads, 
        sortDirection: sortByPrice 
      });
    } else {
      // Fallback: сортировка в основном потоке
      setTimeout(() => {
        const adsCopy = [...ads];
        if (sortByPrice === 'asc') {
          adsCopy.sort((a, b) => a.price - b.price);
        } else if (sortByPrice === 'desc') {
          adsCopy.sort((a, b) => b.price - a.price);
        }
        setSortedAds(adsCopy);
        setIsSorting(false);
      }, 0);
    }
  }, [sortByPrice, ads]);

  // Форматирование даты
  const formatDate = (dateString?: string): string => {
    if (!dateString) return 'Сегодня';
    const date = new Date(dateString);
    return date.toLocaleDateString('ru-RU');
  };

  const handleLogin = () => setIsAuthenticated(true);
  const handleLogout = () => setIsAuthenticated(false);

  // Функции сортировки
  const sortByPriceAsc = () => setSortByPrice('asc');
  const sortByPriceDesc = () => setSortByPrice('desc');
  const clearSort = () => setSortByPrice(null);

  return {
    ads: sortedAds, // Возвращаем отсортированные объявления
    isAuthenticated,
    loading: loading || isSorting, // Показываем загрузку при сортировке тоже
    error,
    sortByPrice,
    handleLogin,
    handleLogout,
    refreshAds: fetchAdverts,
    // Экспортируем функции сортировки
    sortByPriceAsc,
    sortByPriceDesc,
    clearSort
  };
};
