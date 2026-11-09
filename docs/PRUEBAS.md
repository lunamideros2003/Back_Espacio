# Pruebas del backend

Las pruebas usan `pytest` y no tocan la base de datos real: `tests/conftest.py`
define `DATABASE_URL=sqlite:///./test_astroia.db` y `AUTO_CREATE_TABLES=1`.

## Comando

```powershell
.\.venv\Scripts\python.exe -m pytest
```

En Linux o Render:

```bash
python -m pytest
```

## Cobertura actual

| Área | Archivos |
| --- | --- |
| Ubicación | `test_coords`, `test_client_ip`, `test_places`, `test_place_router` |
| Geocodificación | `test_geocode`, `test_reverse_place`, `test_ip_lookup` |
| Caché y etiquetas | `test_place_cache`, `test_place_label` |
| Carta celeste | `test_chart`, `test_projection` |
| Configuración | `test_config` |
| Autenticación | `test_auth` |
| Salud | `test_health` |
| Respaldo | `test_fallback_place` |

## Buenas prácticas

- Nunca llamar a servicios externos: se usa `monkeypatch` sobre `httpx`.
- Cada prueba debe poder correr sola y en cualquier orden.
- Los nombres de las pruebas van en inglés y describen el comportamiento.
- Si se agrega un servicio nuevo, se agrega su archivo `test_<servicio>.py`.
