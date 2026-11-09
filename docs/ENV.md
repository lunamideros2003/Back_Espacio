# Variables de entorno

Todas se leen con `pydantic-settings` desde `.env` o desde el panel de Render.

| Variable | Por defecto | Uso |
| --- | --- | --- |
| `PORT` | `8000` | Puerto de uvicorn |
| `DATABASE_URL` | `sqlite:///./astroia.db` | SQLAlchemy; en producción, Supabase |
| `AUTO_CREATE_TABLES` | `true` | Crear tablas al arrancar |
| `JWT_SECRET` | valor de desarrollo | Firma de tokens |
| `JWT_EXPIRE_MINUTES` | `10080` | Duración del token |
| `NASA_API_KEY` | `DEMO_KEY` | APOD |
| `GROQ_API_KEY` | vacío | Chatbot |
| `CORS_ORIGINS` | vacío | Orígenes extra separados por coma |

## Supabase

Usa la cadena **Session Pooler** (puerto 5432) o la **Direct connection**.
El backend normaliza `postgres://` a `postgresql://` automáticamente.

```env
DATABASE_URL=postgresql://postgres.xxxx:PASSWORD@aws-0-us-east-1.pooler.supabase.com:5432/postgres
AUTO_CREATE_TABLES=false
JWT_SECRET=una-cadena-larga-y-aleatoria
```

## Reglas

- En producción `AUTO_CREATE_TABLES=false` si aplicaste `supabase/schema.sql`.
- `JWT_SECRET` debe tener al menos 32 caracteres.
- Nunca se exponen estas variables al frontend.
- Después de cambiarlas, reinicia el servicio en Render.
