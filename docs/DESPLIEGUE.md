# Despliegue del backend

## Render

1. Crea un **Web Service** desde el repositorio `Back_Espacio`.
2. Runtime: Python.
3. Build: `pip install -r requirements.txt`.
4. Start: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`.
5. Health check: `/api/health`.
6. Variables:
   - `DATABASE_URL` (Supabase, ver `docs/SUPABASE.md`)
   - `AUTO_CREATE_TABLES=0` después del primer arranque
   - `JWT_SECRET` largo y aleatorio
   - `NASA_API_KEY`
   - `AI_PROVIDER`, `GROQ_API_KEY`, `GEMINI_API_KEY` (opcionales)
   - `CORS_ORIGINS` si usas otro dominio además de Vercel

`render.yaml` describe el servicio. No crea una base de datos propia: usa la de
Supabase.

## Local

```bash
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 4000
```

Usuario demo: `luna@astroia.dev` / `astroia123`.

## Verificación

```bash
curl http://localhost:4000/api/health
curl http://localhost:4000/api/health/db
curl "http://localhost:4000/api/place/search?q=Bogota"
.venv\Scripts\python.exe -m pytest
```

## Notas

- El backend no usa `--reload` en producción.
- Si Supabase está en el plan free, el primer request tras una pausa puede
  tardar unos segundos.
- `CORS_ORIGINS` se suma a los orígenes por defecto; no reemplaza Vercel.
