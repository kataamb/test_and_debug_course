import { useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import { useAdvert, useDeleteAdvert } from '../../api/client/hooks/useAdverts';

export const useAdPageViewModel = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { user, isAuthenticated } = useAuth();

  // Используем готовый хук useAdvert
  const {
    data: advert,
    loading: advertLoading,
    error,
    fetchAdvert
  } = useAdvert();

  const {
    loading: deleteLoading,
    deleteAdvert
  } = useDeleteAdvert();

  // Загружаем объявление когда появляется id
  useEffect(() => {
    if (id) {
      console.log('Загружаем объявление ID:', id);
      fetchAdvert(id);
    }
  }, [id]); // Только id как зависимость

  // Вычисляемые значения
  const isOwner = advert?.is_created || false;
  const isLiked = advert?.is_liked || false;
  const isBought = advert?.is_bought || false;



  const handleToggleLike = () => {
    if (!isAuthenticated) {
      alert('Войдите, чтобы добавлять в избранное');
      navigate('/login');
      return;
    }
    alert('Функция "Избранное" скоро будет доступна');
  };

  const handleEdit = () => {
    if (id) navigate(`/adverts/${id}/edit`);
  };

  const handleDelete = async () => {
    if (!id) return;

    if (!window.confirm('Вы уверены, что хотите удалить объявление?')) {
      return;
    }

    try {
      await deleteAdvert(id);
      alert('Объявление удалено');
      navigate('/adverts');
    } catch (error) {
      console.error('Ошибка удаления:', error);
      alert('Не удалось удалить объявление');
    }
  };

  const handleBuy = () => {
    if (!isAuthenticated) {
      alert('Войдите, чтобы купить товар');
      navigate('/login');
      return;
    }

    if (!advert) return;

    if (window.confirm(`Купить "${advert.title}" за ${advert.price} ₽?`)) {
      alert('Функция "Купить" скоро будет доступна');
    }
  };

  return {
    ad: advert,
    isLoading: advertLoading || deleteLoading,
    isAuthenticated,
    isOwner,
    isLiked,
    isBought,
    error,
    handleToggleLike,
    handleEdit,
    handleDelete,
    handleBuy
  };
};