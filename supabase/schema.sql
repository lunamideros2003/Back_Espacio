-- AstroIA schema for Supabase Postgres.
-- The API can create these tables automatically (AUTO_CREATE_TABLES=1),
-- but running this file in the Supabase SQL Editor is the explicit path.

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(120) NOT NULL,
    email VARCHAR(180) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    level VARCHAR(32) NOT NULL DEFAULT 'beginner',
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    city VARCHAR(120),
    created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS ix_users_email ON users (email);

CREATE TABLE IF NOT EXISTS celestial_objects (
    id SERIAL PRIMARY KEY,
    slug VARCHAR(80) NOT NULL UNIQUE,
    name VARCHAR(160) NOT NULL,
    type VARCHAR(40) NOT NULL,
    constellation VARCHAR(80),
    magnitude DOUBLE PRECISION,
    ra_hours DOUBLE PRECISION,
    dec_deg DOUBLE PRECISION,
    distance VARCHAR(160),
    diameter VARCHAR(160),
    fun_fact TEXT NOT NULL,
    explain_beginner TEXT NOT NULL,
    explain_medium TEXT NOT NULL,
    explain_advanced TEXT NOT NULL,
    image_query VARCHAR(160) NOT NULL,
    tags VARCHAR(255) NOT NULL,
    best_months VARCHAR(160) NOT NULL,
    astronomy_body VARCHAR(40)
);

CREATE INDEX IF NOT EXISTS ix_celestial_objects_slug ON celestial_objects (slug);
CREATE INDEX IF NOT EXISTS ix_celestial_objects_type ON celestial_objects (type);

CREATE TABLE IF NOT EXISTS quiz_questions (
    id SERIAL PRIMARY KEY,
    object_id INTEGER REFERENCES celestial_objects (id) ON DELETE SET NULL,
    level VARCHAR(32) NOT NULL,
    question TEXT NOT NULL,
    options TEXT NOT NULL,
    correct_index INTEGER NOT NULL,
    explanation TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS quiz_attempts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users (id) ON DELETE CASCADE,
    score INTEGER NOT NULL,
    total INTEGER NOT NULL,
    level VARCHAR(32) NOT NULL,
    created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS observations (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users (id) ON DELETE CASCADE,
    object_id INTEGER NOT NULL REFERENCES celestial_objects (id) ON DELETE CASCADE,
    notes TEXT,
    visible BOOLEAN NOT NULL DEFAULT TRUE,
    date TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS chat_messages (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users (id) ON DELETE SET NULL,
    role VARCHAR(20) NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT now()
);
