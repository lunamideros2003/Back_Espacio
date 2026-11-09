# Esquema SQL de Supabase

- `schema.sql`: todo el esquema en un solo archivo (recomendado).
- `01_users.sql` ... `05_chat.sql`: los mismos objetos por dominio.

El backend crea estas tablas automáticamente con `AUTO_CREATE_TABLES=1`, pero
ejecutar el SQL en **Supabase → SQL Editor** deja el esquema explícito y
versionado.

## Orden

1. `01_users.sql`
2. `02_celestial_objects.sql`
3. `03_quiz.sql`
4. `04_observations.sql`
5. `05_chat.sql`

Los archivos usan `CREATE TABLE IF NOT EXISTS`, así que se pueden ejecutar más
de una vez sin romper nada.

## Después del SQL

```bash
python scripts/init_db.py
python scripts/count_rows.py
```

La guía completa está en `../docs/SUPABASE.md`.
