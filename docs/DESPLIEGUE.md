# Despliegue del backend

## Orden

1. Supabase: crear proyecto y ejecutar `supabase/schema.sql`.
2. Render: configurar variables y desplegar.
3. Vercel: apuntar `VITE_API_URL` al backend.

## Render

- Tipo: Web Service
- Runtime: Python
- Build: `pip install -r requirements.txt`
- Start: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Health check: `/api/health`

Variables mínimas:

```env
DATABASE_URL=postgresql://postgres.<ref>:<PASSWORD>@aws-1-us-west-2.pooler.supabase.com:6543/postgres?sslmode=require
AUTO_CREATE_TABLES=0
JWT_SECRET=<clave-larga>
```

También se puede omitir `DATABASE_URL` y usar `SUPABASE_DB_HOST`,
`SUPABASE_DB_PORT`, `SUPABASE_DB_NAME`, `SUPABASE_DB_USER` y
`SUPABASE_DB_PASSWORD`.

## Comprobar

```bash
curl https://TU-API.onrender.com/api/health
curl https://TU-API.onrender.com/api/health/db
curl "https://TU-API.onrender.com/api/place/search?q=Pasto"
```

El plan free de Render duerme el servicio. La primera petición puede tardar
hasta un minuto.

## CORS

El dominio `https://fron-espacio.vercel.app` ya está permitido. Para dominios
nuevos, agregarlos en `CORS_ORIGINS` separados por coma.
