-- Создаем новую схему (только один раз)

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

-- Таблица categoriesS
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