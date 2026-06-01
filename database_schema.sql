-- ============================================
-- FSTR Mountain Passes API - Database Schema
-- ============================================

-- 1. Таблица пользователей
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    fam VARCHAR(255),
    name VARCHAR(255),
    otc VARCHAR(255),
    phone VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);

-- 2. Таблица перевалов
CREATE TABLE IF NOT EXISTS passes (
    id SERIAL PRIMARY KEY,
    beauty_title VARCHAR(255),
    title VARCHAR(255) NOT NULL,
    other_titles TEXT,
    connect TEXT,
    add_time TIMESTAMP,
    latitude DECIMAL(9,6) NOT NULL CHECK (latitude BETWEEN -90 AND 90),
    longitude DECIMAL(9,6) NOT NULL CHECK (longitude BETWEEN -180 AND 180),
    height INTEGER CHECK (height >= 0),
    level_winter VARCHAR(10),
    level_spring VARCHAR(10),
    level_summer VARCHAR(10),
    level_autumn VARCHAR(10),
    status VARCHAR(20) DEFAULT 'new' NOT NULL
        CHECK (status IN ('new', 'pending', 'accepted', 'rejected')),
    user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_pass_location UNIQUE (latitude, longitude, title)
);

-- Индексы для оптимизации запросов
CREATE INDEX IF NOT EXISTS idx_passes_status ON passes(status);
CREATE INDEX IF NOT EXISTS idx_passes_add_time ON passes(add_time DESC);
CREATE INDEX IF NOT EXISTS idx_passes_coords ON passes(latitude, longitude);
CREATE INDEX IF NOT EXISTS idx_passes_user ON passes(user_id);

-- 3. Таблица изображений
CREATE TABLE IF NOT EXISTS pass_images (
    id SERIAL PRIMARY KEY,
    pass_id INTEGER NOT NULL REFERENCES passes(id) ON DELETE CASCADE,
    data BYTEA NOT NULL,
    title VARCHAR(255),
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_pass_images_pass_id ON pass_images(pass_id);