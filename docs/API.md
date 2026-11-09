# API de AstroIA

Base local: `http://localhost:4000`. Documentación interactiva: `/docs`.

## Salud

| Método | Ruta | Descripción |
| --- | --- | --- |
| GET | `/api/health` | Proceso vivo |
| GET | `/api/health/db` | Prueba `SELECT 1` contra SQLite/Postgres |
| GET | `/api/debug/cors` | Origen recibido y orígenes permitidos |

`/api/health/db` responde `200` con `{ "ok": true, "database": "up" }` o `503`
con `{ "error": "Base de datos no disponible" }`.

## Ubicación

| Método | Ruta | Descripción |
| --- | --- | --- |
| GET | `/api/place?lat=&lng=` | Resuelve etiqueta y origen de la ubicación |
| GET | `/api/place/search?q=` | Busca ciudades por nombre (mínimo 2 letras) |

Orden de resolución: coordenadas del navegador → perfil → IP pública →
fallback Bogotá. La respuesta siempre trae `latitude`, `longitude`, `label` y
`source` (`browser`, `profile`, `ip`, `search`, `fallback`).

La búsqueda devuelve `{ "results": [{ "latitude", "longitude", "label", "source" }] }`
y usa caché en memoria.

## Cielo

| Método | Ruta | Descripción |
| --- | --- | --- |
| GET | `/api/observe/tonight?lat=&lng=&date=` | Recomendaciones, clima, Luna e ISS |
| GET | `/api/sky/chart?lat=&lng=&date=` | Carta circular con estrellas, líneas y cuerpos |
| GET | `/api/iss/track?minutes=&step=` | Órbita reciente de la ISS |
| GET | `/api/iss/overhead?lat=&lng=&hours=` | Próximos pases visibles |
| GET | `/api/apod` | Foto astronómica del día (NASA) |

`date` es ISO 8601. Si se omite, se usa `datetime.utcnow()`.

## Catálogo y aprendizaje

| Método | Ruta | Descripción |
| --- | --- | --- |
| GET | `/api/objects?type=&q=` | Catálogo filtrable |
| GET | `/api/objects/{slug}?level=` | Detalle con explicación por nivel |
| GET | `/api/quiz/generate?level=&count=` | Preguntas aleatorias |
| POST | `/api/quiz/submit` | Corrige y guarda el intento |
| GET | `/api/quiz/scores` | Puntuaciones del usuario |

## Cuenta

| Método | Ruta | Descripción |
| --- | --- | --- |
| POST | `/api/auth/register` | Crea usuario y devuelve JWT |
| POST | `/api/auth/login` | Login con JWT |
| GET | `/api/auth/me` | Usuario actual |
| PATCH | `/api/auth/me` | Actualiza nombre, nivel, ciudad o coordenadas |
| POST | `/api/observe/log` | Guarda una observación |
| GET | `/api/observe/mine` | Observaciones del usuario |

Las rutas privadas esperan `Authorization: Bearer <token>`.

## Chat

| Método | Ruta | Descripción |
| --- | --- | --- |
| POST | `/api/chat` | Chat astronómico multi-proveedor |
| POST | `/api/chat/classify` | Clasifica una luz descrita por el usuario |

Los errores usan `{ "error": "mensaje en español" }`.
