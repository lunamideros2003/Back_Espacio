# Render

## Servicio

- Nombre: `astroia-api`
- Runtime: Python
- Plan: free
- Build: `pip install -r requirements.txt`
- Start: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Health check: `/api/health`

## Variables

| Variable | Valor |
| --- | --- |
| `DATABASE_URL` | Cadena de Supabase (opcional si usas las demás) |
| `SUPABASE_DB_HOST` | `aws-1-us-west-2.pooler.supabase.com` |
| `SUPABASE_DB_PORT` | `6543` |
| `SUPABASE_DB_NAME` | `postgres` |
| `SUPABASE_DB_USER` | `postgres.<project-ref>` |
| `SUPABASE_DB_PASSWORD` | Contraseña de la base |
| `AUTO_CREATE_TABLES` | `1` |
| `JWT_SECRET` | Clave larga y aleatoria |
| `NASA_API_KEY` | Clave o `DEMO_KEY` |
| `AI_PROVIDER` | `auto` |
| `GROQ_API_KEY` | Opcional |
| `GEMINI_API_KEY` | Opcional |
| `CORS_ORIGINS` | Opcional |

## Creación automática

Con `AUTO_CREATE_TABLES=1` el servicio aplica `supabase/schema.sql` en cada
arranque. En los logs aparece:

```
[AstroIA] Esquema aplicado: 9 sentencias.
```

No borra datos ni duplica tablas. Guía completa en
[`AUTO_CREATE.md`](AUTO_CREATE.md).

## Después del deploy

1. Abrir `https://TU-API.onrender.com/api/health`.
2. Abrir `https://TU-API.onrender.com/api/health/db`.
3. Abrir `https://TU-API.onrender.com/api/place/search?q=Bogota`.
4. Revisar **Logs** y confirmar las 9 sentencias.
5. Si algo falla, revisar el detalle del error en **Logs**.

## Si el deploy falla

El backend ahora imprime la causa antes de seguir:

```
[AstroIA] Base de datos: postgresql://postgres.<ref>:***@host:6543/postgres
[AstroIA] ERROR de base de datos: OperationalError: password authentication failed
```

La API arranca igual para que puedas abrir `/api/health/db` y ver los logs.

Revisa en este orden:

1. Si aparece `DATABASE_URL tiene prioridad`, borra `DATABASE_URL` en Render o
   ponla correcta. Mientras exista, las variables `SUPABASE_DB_*` se ignoran.
2. `SUPABASE_DB_USER` debe ser `postgres.<project-ref>`, no el texto de ejemplo.
3. `SUPABASE_DB_PASSWORD` es la contraseña de la base, no la `secret key`.
4. Prueba `SUPABASE_DB_PORT=6543` (pooler) y, si falla, `5432`.

La forma más simple: Supabase → **Connect** → **Transaction pooler**, copiar la
URI completa (incluye la contraseña) y pegarla en `DATABASE_URL`.

## Errores comunes

| Error | Solución |
| --- | --- |
| `could not translate host name` | Revisar `SUPABASE_DB_HOST` |
| `password authentication failed` | Resolver la contraseña en Supabase y actualizarla |
| `SSL connection is required` | Agregar `?sslmode=require` |
| `relation does not exist` | Poner `AUTO_CREATE_TABLES=1` y redeploy |
| `DATABASE_URL tiene prioridad` | Borrar `DATABASE_URL` o corregirla |
| Primera carga lenta | El servicio free está despertando |
