import { useState, useCallback } from 'react';
import { AdvertsApi } from '../api/adverts-api';
import type {
  AdvertCreateDTO,
  AdvertUpdateFullDTO,
  AdvertUpdatePartialDTO,
  AdvertSearchRequestDTO
} from '../models';

const advertsApi = new AdvertsApi();



export const useAdverts = () => {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchAdverts = useCallback(async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await advertsApi.getAllAdvertsApiV1AdvertsGet();
      setData(response.data);
      return response.data;
    } catch (err: any) {
      const message = err.response?.data?.detail || err.message || 'Ошибка';
      setError(message);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  return {
    data,
    loading,
    error,
    fetchAdverts,
    refetch: fetchAdverts
  };
};


export const useAdvert = () => {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchAdvert = useCallback(async (advertId: string) => {
    if (!advertId) return;

    setLoading(true);
    setError(null);

    try {
      const response = await advertsApi.getAdvertApiV1AdvertsAdvertIdGet(advertId);
      setData(response.data);
      return response.data;
    } catch (err: any) {
      const message = err.response?.data?.detail || err.message || 'Ошибка';
      setError(message);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  return {
    data,
    loading,
    error,
    fetchAdvert,
    refetch: fetchAdvert
  };
};


export const useCreateAdvert = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [data, setData] = useState<any>(null);

  const createAdvert = useCallback(async (advertData: AdvertCreateDTO) => {
    setLoading(true);
    setError(null);

    try {
      const response = await advertsApi.createAdvertApiV1AdvertsPost(advertData);
      setData(response.data);
      return response.data;
    } catch (err: any) {
      const message = err.response?.data?.detail || err.message || 'Ошибка';
      setError(message);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  return {
    data,
    loading,
    error,
    createAdvert
  };
};


export const useDeleteAdvert = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);

  const deleteAdvert = useCallback(async (advertId: string) => {
    setLoading(true);
    setError(null);
    setSuccess(false);

    try {
      await advertsApi.deleteAdvertApiV1AdvertsAdvertIdDelete(advertId);
      setSuccess(true);
      return true;
    } catch (err: any) {
      const message = err.response?.data?.detail || err.message || 'Ошибка';
      setError(message);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  return {
    loading,
    error,
    success,
    deleteAdvert
  };
};


export const useUpdateAdvertFull = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [data, setData] = useState<any>(null);

  const updateAdvertFull = useCallback(async (advertId: string, advertData: AdvertUpdateFullDTO) => {
    setLoading(true);
    setError(null);

    try {
      const response = await advertsApi.updateAdvertFullApiV1AdvertsAdvertIdPut(advertId, advertData);
      setData(response.data);
      return response.data;
    } catch (err: any) {
      const message = err.response?.data?.detail || err.message || 'Ошибка';
      setError(message);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  return {
    data,
    loading,
    error,
    updateAdvertFull
  };
};


export const useUpdateAdvertPartial = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [data, setData] = useState<any>(null);

  const updateAdvertPartial = useCallback(async (advertId: string, advertData: AdvertUpdatePartialDTO) => {
    setLoading(true);
    setError(null);

    try {
      const response = await advertsApi.updateAdvertPartialApiV1AdvertsAdvertIdPatch(advertId, advertData);
      setData(response.data);
      return response.data;
    } catch (err: any) {
      const message = err.response?.data?.detail || err.message || 'Ошибка';
      setError(message);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  return {
    data,
    loading,
    error,
    updateAdvertPartial
  };
};


export const useSearchAdverts = () => {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const searchAdverts = useCallback(async (searchParams: AdvertSearchRequestDTO) => {
    setLoading(true);
    setError(null);

    try {
      const response = await advertsApi.getSearchAdvertsApiV1AdvertsSearchPost(searchParams);
      setData(response.data);
      return response.data;
    } catch (err: any) {
      const message = err.response?.data?.detail || err.message || 'Ошибка';
      setError(message);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  return {
    data,
    loading,
    error,
    searchAdverts
  };
};


export const useMyAdverts = () => {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchMyAdverts = useCallback(async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await advertsApi.getMyAdvertsApiV1AdvertsCreatedGet();
      setData(response.data);
      return response.data;
    } catch (err: any) {
      const message = err.response?.data?.detail || err.message || 'Ошибка';
      setError(message);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  return {
    data,
    loading,
    error,
    fetchMyAdverts,
    refetch: fetchMyAdverts
  };
};


export const useLikedAdverts = () => {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchLikedAdverts = useCallback(async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await advertsApi.getLikedAdvertsApiV1AdvertsLikedGet();
      setData(response.data);
      return response.data;
    } catch (err: any) {
      const message = err.response?.data?.detail || err.message || 'Ошибка';
      setError(message);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  return {
    data,
    loading,
    error,
    fetchLikedAdverts,
    refetch: fetchLikedAdverts
  };
};


export const useDealsAdverts = () => {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchDealsAdverts = useCallback(async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await advertsApi.getInDealsAdvertsApiV1AdvertsDealsGet();
      setData(response.data);
      return response.data;
    } catch (err: any) {
      const message = err.response?.data?.detail || err.message || 'Ошибка';
      setError(message);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  return {
    data,
    loading,
    error,
    fetchDealsAdverts,
    refetch: fetchDealsAdverts
  };
};