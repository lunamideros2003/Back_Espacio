# AstroIA API

Hice este backend con FastAPI para que la página tenga datos del cielo, cuentas
y chatbot. En mi computador uso SQLite y en producción uso Supabase Postgres.

## Cómo arrancarlo

```bash
cd Back_Espacio
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 4000
```

La API queda en http://localhost:4000 y la documentación en
http://localhost:4000/docs.

## Qué hace

- Calcula estrellas y planetas con PyEphem.
- Busca mi ubicación automáticamente, sin pedir latitud ni longitud.
- Da recomendaciones para esta noche con el clima real.
- Muestra la ISS y sus pases visibles.
- Responde en el chatbot con Groq, Gemini o en modo local.
- Guarda usuarios, quiz, observaciones y mensajes.

## Base de datos

Con `AUTO_CREATE_TABLES=1` el backend crea las tablas solo al arrancar. No borra
datos y puedo ejecutarlo varias veces sin errores.

```env
AUTO_CREATE_TABLES=1
SUPABASE_DB_HOST=aws-1-us-west-2.pooler.supabase.com
SUPABASE_DB_PORT=6543
SUPABASE_DB_NAME=postgres
SUPABASE_DB_USER=postgres.<ref>
SUPABASE_DB_PASSWORD=<PASSWORD>
```

Si tengo `DATABASE_URL`, esa manda. Los detalles están en
[`docs/AUTO_CREATE.md`](docs/AUTO_CREATE.md).

## Pruebas

```bash
.venv\Scripts\python.exe -m pytest
```

## Servicios gratuitos que uso

- NASA APOD e Images (`DEMO_KEY` o mi clave de https://api.nasa.gov)
- Open-Meteo para el clima y las ciudades
- ipwho.is para la ubicación aproximada
- BigDataCloud y Nominatim para nombres de lugares
- Where The ISS At para la ISS
- Groq o Gemini para el chatbot, si tengo clave

## Más detalles

- `docs/ARQUITECTURA.md`
- `docs/API.md`
- `docs/UBICACION.md`
- `docs/SUPABASE.md`
- `docs/AUTO_CREATE.md`
- `docs/ENV.md`
- `docs/DESPLIEGUE.md`
- `docs/RENDER.md`
- `docs/VERCEL.md`
- `docs/SEGURIDAD.md`
- `docs/MIGRACION.md`
- `docs/PRUEBAS.md`
- `docs/CHECKLIST.md`
- `supabase/README.md`
