# AstroIA — API (FastAPI)

Explorador inteligente del universo. SQLite en desarrollo y **Supabase
Postgres** en producción.

## Cómo arrancar

```bash
cd Back_Espacio
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 4000
```

API: http://localhost:4000  
Docs: http://localhost:4000/docs

Usuario demo: `luna@astroia.dev` / `astroia123`

## Qué incluye

- Ubicación automática sin latitud/longitud manuales: GPS → perfil → IP →
  búsqueda de ciudad → fallback.
- Carta celeste circular con catálogo J2000 y proyección propia.
- Recomendaciones nocturnas con clima real (Open-Meteo).
- ISS: posición, órbita y pases visibles.
- Chatbot multi-proveedor (Groq, Gemini o modo local).
- Auth JWT, quiz, observaciones y perfil.
- Tests con pytest (sin llamadas reales a internet).

## Supabase

Guía paso a paso: [`docs/SUPABASE.md`](docs/SUPABASE.md). Esquema listo para
pegar en el SQL Editor: [`supabase/schema.sql`](supabase/schema.sql).

Variables separadas opcionales:

```env
SUPABASE_DB_HOST=aws-1-us-west-2.pooler.supabase.com
SUPABASE_DB_PORT=6543
SUPABASE_DB_NAME=postgres
SUPABASE_DB_USER=postgres.<ref>
SUPABASE_DB_PASSWORD=<PASSWORD>
```

Si `DATABASE_URL` está definido, tiene prioridad.

```bash
.venv\Scripts\python.exe scripts/check_db.py
.venv\Scripts\python.exe scripts/init_db.py
.venv\Scripts\python.exe scripts/count_rows.py
```

## Tests

```bash
.venv\Scripts\python.exe -m pytest
```

## APIs gratuitas usadas

- NASA APOD e Images API (`DEMO_KEY` o tu clave en https://api.nasa.gov)
- Open-Meteo (nubes, visibilidad y búsqueda de ciudades)
- ipwho.is (ubicación aproximada por IP)
- BigDataCloud / Nominatim (etiqueta de una coordenada)
- Where The ISS At
- Opcional: Groq (`GROQ_API_KEY`) para el chatbot con Llama

Las posiciones de planetas y estrellas se calculan en el servidor con
**PyEphem**.

## Documentación

- `docs/ARQUITECTURA.md`
- `docs/API.md`
- `docs/UBICACION.md`
- `docs/SUPABASE.md`
- `docs/ENV.md`
- `docs/DESPLIEGUE.md`
- `docs/RENDER.md`
- `docs/VERCEL.md`
- `docs/SEGURIDAD.md`
- `docs/MIGRACION.md`
- `docs/PRUEBAS.md`
- `docs/CHECKLIST.md`
- `supabase/README.md`
