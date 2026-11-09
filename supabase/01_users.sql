-- Users and profiles.

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
