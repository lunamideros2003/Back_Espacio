# Ubicación automática (backend)

`app/services/places.py` implementa la cascada:

1. `browser`: lat/lng válidas enviadas por el navegador.
2. `profile`: coordenadas guardadas del usuario autenticado.
3. `ip`: geolocalización aproximada de la IP pública (`ipwho.is`).
4. `fallback`: Bogotá como cielo de ejemplo.

La UI puede añadir una quinta fuente, `search`, cuando el usuario elige una
ciudad por nombre; esa ubicación se guarda 12 h en el navegador y se envía como
coordenadas en las siguientes peticiones.

## Piezas

- `client_ip.py`: lee `X-Forwarded-For`, `X-Real-IP` o el host de conexión y
  descarta IPs privadas.
- `ip_lookup.py`: consulta `ipwho.is` con caché de 1 h.
- `reverse_place.py`: etiqueta una coordenada con BigDataCloud y, si falla,
  Nominatim. Caché de 24 h por coordenada redondeada.
- `geocode.py`: busca ciudades con Open-Meteo Geocoding (caché de 24 h).
- `place_cache.py`: caché TTL en memoria.
- `coords.py`: parseo y validación de rangos.
- `place_label.py`: arma etiquetas legibles ("Bogotá, Colombia").

## Por qué no se piden coordenadas

Escribir números es propenso a errores y rompe la experiencia. La API acepta
lat/lng para integraciones, pero el flujo normal es GPS o nombre de ciudad.
