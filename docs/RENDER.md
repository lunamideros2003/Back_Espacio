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
| `AUTO_CREATE_TABLES` | `0` |
| `JWT_SECRET` | Clave larga y aleatoria |
| `NASA_API_KEY` | Clave o `DEMO_KEY` |
| `AI_PROVIDER` | `auto` |
| `GROQ_API_KEY` | Opcional |
| `GEMINI_API_KEY` | Opcional |
| `CORS_ORIGINS` | Opcional |

## Después del deploy

1. Abrir `https://TU-API.onrender.com/api/health`.
2. Abrir `https://TU-API.onrender.com/api/health/db`.
3. Abrir `https://TU-API.onrender.com/api/place/search?q=Bogota`.
4. Si algo falla, revisar **Logs** en Render.

## Errores comunes

| Error | Solución |
| --- | --- |
| `could not translate host name` | Revisar `SUPABASE_DB_HOST` |
| `password authentication failed` | Revisar `SUPABASE_DB_PASSWORD` |
| `SSL connection is required` | Agregar `?sslmode=require` |
| `relation does not exist` | Ejecutar `supabase/schema.sql` |
| Primera carga lenta | El servicio free está despertando |
