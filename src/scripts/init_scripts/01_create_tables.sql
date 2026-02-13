-- Создаем новую схему (только один раз)
drop schema adv_uuid;
CREATE SCHEMA IF NOT EXISTS adv_uuid;

-- Включаем расширение для UUID (только один раз)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Таблица profiles
CREATE TABLE IF NOT EXISTS adv_uuid.profiles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    nickname VARCHAR(50) NOT NULL UNIQUE,
    fio VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    phone_number VARCHAR(20),
    password VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Таблица categories
CREATE TABLE IF NOT EXISTS adv_uuid.categories (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(50) NOT NULL UNIQUE
);

-- Таблица customers
CREATE TABLE IF NOT EXISTS adv_uuid.customers (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    profile_id UUID NOT NULL REFERENCES adv_uuid.profiles(id),
    rating INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Таблица sellers
CREATE TABLE IF NOT EXISTS adv_uuid.sellers (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    profile_id UUID NOT NULL REFERENCES adv_uuid.profiles(id),
    rating INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Таблица adverts
CREATE TABLE IF NOT EXISTS adv_uuid.adverts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    content TEXT NOT NULL,
    description TEXT,
    id_category UUID NOT NULL REFERENCES adv_uuid.categories(id),
    price INTEGER NOT NULL CHECK (price >= 0),
    id_seller UUID NOT NULL REFERENCES adv_uuid.sellers(id),
    date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Таблица deals
CREATE TABLE IF NOT EXISTS adv_uuid.deals (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    id_advert UUID NOT NULL REFERENCES adv_uuid.adverts(id),
    id_customer UUID NOT NULL REFERENCES adv_uuid.customers(id),
    date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    address TEXT NOT NULL
);

-- Таблица likes
CREATE TABLE IF NOT EXISTS adv_uuid.likes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    id_customer UUID NOT NULL REFERENCES adv_uuid.customers(id),
    id_advert UUID NOT NULL REFERENCES adv_uuid.adverts(id),
    date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (id_customer, id_advert) -- Один лайк на объявление от пользователя
);

CREATE TABLE IF NOT EXISTS adv_uuid.history_deals (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    id_deal UUID NOT NULL REFERENCES adv_uuid.deals(id) ON DELETE CASCADE,
    id_customer UUID NOT NULL REFERENCES adv_uuid.customers(id) ON DELETE CASCADE,
    status INTEGER NOT NULL,  -- например: 0 = активна, 1 = завершена, 2 = отменена
    date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Индексы для улучшения производительности
CREATE INDEX IF NOT EXISTS idx_adverts_category ON adv_uuid.adverts(id_category);
CREATE INDEX IF NOT EXISTS idx_adverts_seller ON adv_uuid.adverts(id_seller);
CREATE INDEX IF NOT EXISTS idx_adverts_created ON adv_uuid.adverts(date_created);
CREATE INDEX IF NOT EXISTS idx_deals_advert ON adv_uuid.deals(id_advert);
CREATE INDEX IF NOT EXISTS idx_deals_customer ON adv_uuid.deals(id_customer);
CREATE INDEX IF NOT EXISTS idx_likes_customer ON adv_uuid.likes(id_customer);
CREATE INDEX IF NOT EXISTS idx_likes_advert ON adv_uuid.likes(id_advert);


CREATE ROLE admin LOGIN PASSWORD 'admin';
GRANT ALL PRIVILEGES ON SCHEMA adv_uuid TO admin;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA adv_uuid  TO admin;


-------------------------------------------------

COPY adv_uuid.categories (id, name)
FROM '/data_tables_uuid/category.csv'
DELIMITER ';'
CSV HEADER;

select * from adv_uuid.categories;


COPY adv_uuid.profiles (id, nickname, fio, email, phone_number, password, created_at)
FROM '/data_tables_uuid/profile.csv'
DELIMITER ';'
CSV HEADER;

 SELECT COUNT(*) FROM adv_uuid.profiles;

-- Загрузка данных в таблицу customers
COPY adv_uuid.customers (id, profile_id, rating, created_at)
FROM '/data_tables_uuid/customer.csv'
DELIMITER ';'
CSV HEADER;

-- Загрузка данных в таблицу sellers
COPY adv_uuid.sellers (id, profile_id, rating, created_at)
FROM '/data_tables_uuid/seller.csv'
DELIMITER ';'
CSV HEADER;

-- Загрузка данных в таблицу adverts
COPY adv_uuid.adverts (id, content, description, id_category, price, id_seller, date_created)
FROM '/data_tables_uuid/advert.csv'
DELIMITER ';'
CSV HEADER;


-- Загрузка данных в таблицу deals
COPY adv_uuid.deals (id, id_advert, id_customer, date_created, address)
FROM '/data_tables_uuid/deal.csv'
DELIMITER ';'
CSV HEADER;

-- Загрузка данных в таблицу likes
COPY adv_uuid.likes (id, id_customer, id_advert, date_created)
FROM '/data_tables_uuid/like.csv'
DELIMITER ';'
CSV HEADER;

-- История сделок
COPY adv_uuid.history_deals(id, id_deal, id_customer, status, date_created)
FROM '/data_tables_uuid/history_deal.csv'
DELIMITER ';'
CSV HEADER;



-----------------------------------------

INSERT INTO adv_uuid.adverts (content, description, id_category, price, id_seller)
VALUES (
    'Ноутбук игровой MSI',
    'Мощный игровой ноутбук с видеокартой RTX 4060, 16GB RAM, SSD 1TB',
    '0bca2980-b4e9-4a26-8494-f0fde2d54744',
    75000,
    '58b5f794-6354-47d2-81b1-81a35306dab8'
)
RETURNING id;




