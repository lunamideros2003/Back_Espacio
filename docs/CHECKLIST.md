# Checklist de despliegue

## Supabase

- [ ] Proyecto creado.
- [ ] Contraseña de la base guardada.
- [ ] `supabase/schema.sql` ejecutado.
- [ ] Tablas visibles en el Table Editor.

## Backend en Render

- [ ] Variables `SUPABASE_DB_*` o `DATABASE_URL` configuradas.
- [ ] `AUTO_CREATE_TABLES=0`.
- [ ] `JWT_SECRET` largo y aleatorio.
- [ ] Deploy exitoso.
- [ ] `/api/health` responde 200.
- [ ] `/api/health/db` responde 200.
- [ ] `/api/place/search?q=Bogota` devuelve resultados.
- [ ] Catálogo sembrado con `scripts/init_db.py`.

## Frontend en Vercel

- [ ] `VITE_API_URL` apunta a Render, sin barra final.
- [ ] Redeploy hecho después de cambiar la variable.
- [ ] Portada con constelación y lugar automático.
- [ ] `/observar` sin coordenadas manuales.
- [ ] `/carta` sin coordenadas manuales.
- [ ] `/iss` fuera del menú pero accesible.

## Pruebas finales

- [ ] Registro de usuario.
- [ ] Login.
- [ ] Guardar una observación.
- [ ] Completar un quiz.
- [ ] Enviar un mensaje al chat.
- [ ] Reiniciar Render y confirmar persistencia.

## Seguridad

- [ ] `.env` fuera de git.
- [ ] Sin `sb_secret` en el repositorio.
- [ ] Sin contraseñas en variables `VITE_*`.
- [ ] Backups revisados.
