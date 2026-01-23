import React from 'react';
import { useAdCardSmallViewModel } from './AdCardSmall.viewModel';

interface AdCardSmallProps {
  id: number;
  content: string;
  price: number;
  date_created: string;
  onCardClick?: () => void;
}

export const AdCardSmall: React.FC<AdCardSmallProps> = (props) => {
  const {
    id,
    content,
    price,

    date_created,
    onCardClick
  } = props;

  // Получаем функцию из viewModel
  const { handleCardClick } = useAdCardSmallViewModel(id);

  // Используем кастомный обработчик или дефолтный
  const clickHandler = onCardClick || handleCardClick;

  return (
    <div onClick={clickHandler}>
      <h3>{content}</h3>
      <div>{price} ₽</div>

      <div>{date_created}</div>
    </div>
  );
};