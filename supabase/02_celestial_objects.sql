-- Celestial catalog used by the explorer and the quiz generator.

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
