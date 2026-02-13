-- Очищаем таблицы (важно для повторных запусков!)
TRUNCATE adv_uuid.categories, adv_uuid.profiles, adv_uuid.sellers,
          adv_uuid.customers, adv_uuid.adverts CASCADE;

-- 1. Категории (3-4 штуки, не 11!)
INSERT INTO adv_uuid.categories (id, name) VALUES
('bd29f255-50ab-4967-bc77-475a5fbe7952', 'Транспорт'),
('37f7590e-aaa2-466f-8b92-113ae31507f9', 'Недвижимость'),
('0bca2980-b4e9-4a26-8494-f0fde2d54744', 'Электроника');

-- 2. Профиль продавца
INSERT INTO adv_uuid.profiles (id, nickname, fio, email, phone_number, password) VALUES
('11111111-1111-1111-1111-111111111111', 'test_seller', 'Test Seller', 'seller@test.com', '+79991234567', 'password123');

-- 3. Продавец (связь с профилем)
INSERT INTO adv_uuid.sellers (id, profile_id, rating) VALUES
('22222222-2222-2222-2222-222222222222', '11111111-1111-1111-1111-111111111111', 0);

-- 4. Профиль покупателя
INSERT INTO adv_uuid.profiles (id, nickname, fio, email, phone_number, password) VALUES
('33333333-3333-3333-3333-333333333333', 'test_customer', 'Test Customer', 'customer@test.com', '+79998765432', 'password123');

-- 5. Покупатель (связь с профилем)
INSERT INTO adv_uuid.customers (id, profile_id, rating) VALUES
('44444444-4444-4444-4444-444444444444', '33333333-3333-3333-3333-333333333333', 0);

-- 6. Объявления (2 штуки)
INSERT INTO adv_uuid.adverts (id, content, description, id_category, price, id_seller, date_created) VALUES
('aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
 'Тестовое объявление 1',
 'Описание тестового объявления 1',
 'bd29f255-50ab-4967-bc77-475a5fbe7952',
 1000,
 '22222222-2222-2222-2222-222222222222',
 NOW());

INSERT INTO adv_uuid.adverts (id, content, description, id_category, price, id_seller, date_created) VALUES
('bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb',
 'Тестовое объявление 2',
 'Описание тестового объявления 2',
 '37f7590e-aaa2-466f-8b92-113ae31507f9',
 2000,
 '22222222-2222-2222-2222-222222222222',
 NOW());