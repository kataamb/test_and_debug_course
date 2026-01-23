// Web Worker для поиска по объявлениям
self.onmessage = function(event) {
  const { ads, searchTerm } = event.data;
  
  if (!searchTerm.trim()) {
    self.postMessage({ result: ads, searchTerm });
    return;
  }
  
  // Поиск по заголовку и описанию
  const filtered = ads.filter(ad => {
    const title = ad.title || '';
    const description = ad.description || '';
    const text = (title + ' ' + description).toLowerCase();
    return text.includes(searchTerm.toLowerCase());
  });
  
  self.postMessage({ 
    result: filtered, 
    searchTerm
  });
};

self.onerror = function(error) {
  console.error('Worker error:', error);
  self.postMessage({ error: 'Worker failed' });
};
