# Variables de entorno

Se leen con `pydantic-settings` desde `.env` o desde Render.

## Servidor

| Variable | Por defecto | Uso |
| --- | --- | --- |
| `PORT` | `8000` | Puerto de uvicorn |
| `DATABASE_URL` | `sqlite:///./astroia.db` | SQLAlchemy |
| `AUTO_CREATE_TABLES` | `true` | Crear tablas al arrancar |
| `DB_POOL_TIMEOUT` | `30` | Espera máxima por una conexión |
| `JWT_SECRET` | valor de desarrollo | Firma de tokens |
| `JWT_EXPIRE_MINUTES` | `10080` | Duración del token |
| `NASA_API_KEY` | `DEMO_KEY` | APOD |
| `GROQ_API_KEY` | vacío | Chatbot |
| `GEMINI_API_KEY` | vacío | Chatbot alternativo |
| `AI_PROVIDER` | `auto` | `auto`, `groq`, `gemini` o `local` |
| `CORS_ORIGINS` | vacío | Orígenes extra separados por coma |

## Supabase

| Variable | Uso |
| --- | --- |
| `SUPABASE_DB_HOST` | Host del pooler |
| `SUPABASE_DB_PORT` | `6543` o `5432` |
| `SUPABASE_DB_NAME` | Normalmente `postgres` |
| `SUPABASE_DB_USER` | `postgres.<project-ref>` |
| `SUPABASE_DB_PASSWORD` | Contraseña de la base |
| `SUPABASE_URL` | Referencia; no se usa todavía |
| `SUPABASE_PUBLISHABLE_KEY` | Solo para Supabase Auth |
| `SUPABASE_SECRET_KEY` | Solo servidor; no es la clave de Postgres |
| `SUPABASE_JWKS_URL` | Solo para validar Auth de Supabase |

Si `DATABASE_URL` está definido, gana sobre `SUPABASE_DB_*`.

## Reglas

- En producción `AUTO_CREATE_TABLES=false` si aplicaste `supabase/schema.sql`.
- `JWT_SECRET` debe tener al menos 32 caracteres.
- Nunca se exponen estas variables al frontend.
- Después de cambiarlas, reinicia el servicio en Render.
