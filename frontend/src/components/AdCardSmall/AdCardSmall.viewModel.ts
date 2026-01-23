import { useNavigate } from 'react-router-dom';

export const useAdCardSmallViewModel = (id: number) => {
  const navigate = useNavigate();

  const handleCardClick = () => {
    console.log('Переход на объявление ID:', id);
    navigate(`/ad/${id}`);
  };

  return {
    handleCardClick
  };
};