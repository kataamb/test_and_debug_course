import { useRef, useCallback, useEffect } from 'react';

export const useSearchWorker = () => {
  const workerRef = useRef(null);

  // Инициализация Worker
  const initWorker = useCallback(() => {
    if (typeof Worker === 'undefined') {
      console.warn('Web Workers not supported');
      return null;
    }

    if (!workerRef.current) {
      try {
        workerRef.current = new Worker(new URL('../workers/search.worker.js', import.meta.url));
      } catch (error) {
        console.error('Failed to create worker:', error);
        return null;
      }
    }
    return workerRef.current;
  }, []);

  // Поиск через Worker
  const searchWithWorker = useCallback((ads, searchTerm) => {
    return new Promise((resolve) => {
      const worker = initWorker();
      
      if (!worker) {
        // Fallback: синхронный поиск если Worker не доступен
        const filtered = ads.filter(ad => {
          const title = ad.title || '';
          const description = ad.description || '';
          const text = (title + ' ' + description).toLowerCase();
          return text.includes(searchTerm.toLowerCase());
        });
        resolve(filtered);
        return;
      }

      // Обработчик сообщений от Worker
      const handleMessage = (event) => {
        worker.removeEventListener('message', handleMessage);
        if (event.data.error) {
          console.error('Worker error:', event.data.error);
          // Fallback
          const filtered = ads.filter(ad => {
            const title = ad.title || '';
            const description = ad.description || '';
            const text = (title + ' ' + description).toLowerCase();
            return text.includes(searchTerm.toLowerCase());
          });
          resolve(filtered);
        } else {
          resolve(event.data.result);
        }
      };

      worker.addEventListener('message', handleMessage);
      worker.postMessage({ ads, searchTerm });
    });
  }, [initWorker]);

  // Очистка при размонтировании
  useEffect(() => {
    return () => {
      if (workerRef.current) {
        workerRef.current.terminate();
        workerRef.current = null;
      }
    };
  }, []);

  return { searchWithWorker };
};
