# Contribuir al backend

## Flujo

1. Rama corta: `feat/lugar`, `fix/carta`, `docs/supabase`.
2. Cambios pequeños y con una sola intención.
3. `python -m pytest` en verde.
4. Commits cortos, en imperativo, sin punto final.
5. Pull request con descripción breve y capturas si cambia la API.

## Estilo

- Python 3.12+, tipos modernos (`str | None`).
- Routers delgados: la lógica vive en `app/services/`.
- Esquemas Pydantic en `app/schemas/`.
- Nombres de código en inglés; textos de usuario en español.
- No se suben `.env`, `*.db` ni credenciales de Supabase.

## Orden de capas

```
router -> service -> datos estáticos / httpx / base de datos
```

Un router no debe importar `httpx` directamente. Un servicio no debe conocer
detalles de FastAPI.

## Documentación

- `docs/API.md`: endpoints.
- `docs/ARQUITECTURA.md`: capas y decisiones.
- `docs/SUPABASE.md`: conexión con Postgres.
- `docs/PRUEBAS.md`: cómo correr y escribir pruebas.
