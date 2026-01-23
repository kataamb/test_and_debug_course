import React from 'react';
import { useAdPageViewModel } from './AdPage.viewModel';

export const AdPage: React.FC = () => {
  const {
    ad,
    isLoading,
    isAuthenticated,
    isOwner,
    isLiked,
    isBought,
    handleBack,
    handleContact,
    handleToggleLike,
    handleEdit,
    handleDelete,
    handleBuy
  } = useAdPageViewModel();

  if (isLoading) {
    return <div>Загрузка объявления...</div>;
  }

  if (!ad) {
    return <div>Объявление не найдено</div>;
  }

  return (
    <div style={{ padding: '20px' }}>

      <div >
        <h1>{ad.content}</h1>

        <div >
          <p><strong>Цена:</strong> {ad.price} ₽</p>
          <p><strong>Описание:</strong> {ad.description}</p>
          <p><strong>Дата публикации:</strong> {ad.date_created}</p>
        </div>



        {/* Кнопки для авторизованных пользователей */}
        {isAuthenticated && (
          <div >

            {/* Кнопка избранного */}
            <button
              onClick={handleToggleLike}

            >
              {isLiked ? 'Убрать из избранного' : 'Добавить в избранное'}
            </button>

            {/* Если пользователь - владелец объявления */}
            {isOwner && (
              <>
                <button
                  onClick={handleEdit}

                >
                  Редактировать
                </button>
                <button
                  onClick={handleDelete}

                >
                 Удалить
                </button>
              </>
            )}

            {/* Если пользователь НЕ владелец */}
            {!isOwner && (
              <>
                {isBought ? (
                  <button
                    disabled

                  >
                    Куплено
                  </button>
                ) : (
                  <button
                    onClick={handleBuy}

                  >
                   Купить
                  </button>
                )}
              </>
            )}
          </div>
        )}

        {/* Сообщение для неавторизованных */}
        {!isAuthenticated && (
          <div >
            <p>Войдите, чтобы добавить в избранное или купить товар</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default AdPage;