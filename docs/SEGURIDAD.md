# Seguridad

## Claves

| Clave | Dónde puede vivir |
| --- | --- |
| `SUPABASE_SECRET_KEY` | Solo en Render o en `.env` local |
| Contraseña de Postgres | Solo en Render o en `.env` local |
| `JWT_SECRET` | Solo en Render o en `.env` local |
| `VITE_API_URL` | Puede ser pública |
| `SUPABASE_PUBLISHABLE_KEY` | Pública, pero hoy no se usa |

## Reglas

- Nunca subir `.env` al repositorio.
- Nunca crear variables `VITE_*` con secretos: terminan en el navegador.
- `SUPABASE_SECRET_KEY` no es la contraseña de la base. La contraseña se
  gestiona en **Database → Settings → Reset database password**.
- Si una clave se filtró, rotarla de inmediato.
- El backend usa el rol Postgres y omite RLS. Si se consulta Supabase desde el
  navegador, activar Row Level Security.

## Revisión

1. `git status` no debe mostrar `.env`.
2. Buscar `sb_secret` y `postgresql://` en el repositorio.
3. Confirmar que Render no imprime la cadena en los logs.
4. Confirmar que Vercel solo tiene `VITE_API_URL`.
