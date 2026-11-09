# Arquitectura del backend

FastAPI + SQLAlchemy 2 + Pydantic. SQLite en desarrollo, Supabase Postgres en
producción.

## Capas

- `app/routers`: endpoints HTTP y validación de entrada.
- `app/schemas`: modelos Pydantic de request (auth, chat, quiz, observe).
- `app/services`: lógica de astronomía, clima, IA, ubicación y proveedores
  externos.
- `app/models.py`: tablas SQLAlchemy.
- `app/auth.py`: hash PBKDF2 y JWT HS256.
- `app/config.py`: settings por variables de entorno.
- `supabase/`: SQL de referencia para crear el esquema.
- `scripts/`: utilidades de base de datos.
- `tests/`: pytest, sin llamadas reales a internet.

## Flujo de una petición

1. El router recibe lat/lng opcionales.
2. `resolve_place` decide la ubicación: GPS → perfil → IP → fallback.
3. Los servicios calculan posiciones (PyEphem), clima (Open-Meteo) e ISS.
4. La respuesta incluye `location.label` y `location.source` para que la UI
   explique de dónde salió la ubicación.

## Astronomía

- `sky.py`: altitud/azimut de estrellas y cuerpos, fase lunar.
- `star_catalog.py`: catálogo J2000 de estrellas brillantes.
- `constellation_lines.py`: segmentos de constelaciones.
- `projection.py`: proyección circular de la carta.
- `chart.py`: ensambla la carta completa.

## Decisiones

- La ubicación nunca se pide como latitud/longitud en la UI.
- El navegador solo habla con la API; Supabase queda detrás.
- Las tablas se crean al arrancar solo si `AUTO_CREATE_TABLES=1`.
- Los tests no dependen de red: los proveedores se inyectan o se prueban sus
  parsers puros.
