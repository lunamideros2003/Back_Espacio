# Conectar AstroIA con Supabase

Supabase se usa como **Postgres gestionado**. El backend sigue hablando
SQLAlchemy y JWT propio; el frontend nunca recibe credenciales de la base de
datos. Es la ruta con menos cambios y la más segura para el proyecto.

## 1. Crear el proyecto

1. Entra a https://supabase.com y crea un proyecto.
2. Guarda la contraseña de la base de datos (la usarás una sola vez).
3. Espera a que termine el aprovisionamiento.

## 2. Copiar la cadena de conexión

En Supabase: **Project Settings → Database → Connection string → URI**.

- **Connection pooling** (recomendado para Render): puerto `6543`.
- **Direct connection**: puerto `5432`.

La cadena se ve así:

```
postgresql://postgres.[project-ref]:[PASSWORD]@aws-0-[region].pooler.supabase.com:6543/postgres?sslmode=require
```

Reglas:

- Si la contraseña tiene `@`, `#`, `/` o `:`, codifícala en URL (`@` → `%40`).
- Mantén `?sslmode=require`.
- No subas la cadena real al repositorio. Va en Render o en tu `.env` local
  (ignorado por git).

## 3. Crear las tablas

Dos opciones equivalentes:

### Opción A — SQL Editor (explícita)

1. Abre **SQL Editor** en Supabase.
2. Pega y ejecuta `supabase/schema.sql` (o los archivos `01_...` a `05_...` en
   orden).

### Opción B — automática al arrancar

Con `AUTO_CREATE_TABLES=1`, `app/main.py` ejecuta
`Base.metadata.create_all()` y `seed_if_empty()` en el primer arranque.

Para producción estable, crea las tablas con la opción A y luego pon
`AUTO_CREATE_TABLES=0` para evitar cambios implícitos.

## 4. Probar desde tu máquina

Crea `Back_Espacio/.env`:

```
DATABASE_URL=postgresql://postgres.[ref]:[PASSWORD]@aws-0-[region].pooler.supabase.com:6543/postgres?sslmode=require
AUTO_CREATE_TABLES=0
JWT_SECRET=una-clave-larga-y-aleatoria
```

Luego:

```bash
.venv\Scripts\python.exe scripts/check_db.py
.venv\Scripts\python.exe scripts/init_db.py
.venv\Scripts\python.exe scripts/count_rows.py
```

Verás el catálogo sembrado en Supabase.

## 5. Render

En **Render → tu servicio → Environment**:

| Variable | Valor |
| --- | --- |
| `DATABASE_URL` | Cadena de Supabase (port 6543) |
| `AUTO_CREATE_TABLES` | `0` (o `1` la primera vez) |
| `JWT_SECRET` | Clave larga y aleatoria |
| `NASA_API_KEY` | Tu clave o `DEMO_KEY` |
| `AI_PROVIDER` | `auto` |
| `GROQ_API_KEY` / `GEMINI_API_KEY` | Opcionales |
| `CORS_ORIGINS` | Opcional; Vercel ya está por defecto |

`render.yaml` ya no crea una base de datos de Render: espera que pegues la de
Supabase. Vuelve a desplegar.

Comprueba:

```bash
curl https://<tu-api>.onrender.com/api/health/db
# {"ok": true, "database": "up"}
```

## 6. Vercel

En **Vercel → Settings → Environment Variables**:

```
VITE_API_URL=https://<tu-api>.onrender.com
```

Redeploy del frontend. El navegador seguirá llamando solo a la API.

## 7. Seguridad

- Nunca pongas `DATABASE_URL`, `service_role` ni la contraseña en variables
  `VITE_*`: todo lo que empieza con `VITE_` termina en el navegador.
- El backend usa el rol Postgres, que **omite RLS**. Si algún día consultas
  Supabase directo desde el navegador, activa Row Level Security y escribe
  políticas por `auth.uid()`.
- Rota la contraseña de la base si alguna vez se filtró.

## 8. Operación

- El plan free de Supabase pausa proyectos inactivos; el primer request puede
  tardar. El backend usa `pool_pre_ping` y recicla conexiones cada 30 minutos.
- Haz backups desde **Database → Backups** antes de cambios grandes.
- Para migraciones versionadas, el siguiente paso es Alembic:
  `AUTO_CREATE_TABLES=0` + `alembic upgrade head`.

## 9. Checklist rápido

- [ ] Proyecto Supabase creado.
- [ ] `supabase/schema.sql` ejecutado.
- [ ] `scripts/init_db.py` sembró el catálogo.
- [ ] `/api/health/db` responde 200 en Render.
- [ ] `VITE_API_URL` apunta a Render en Vercel.
- [ ] El login y el quiz guardan datos en Supabase.
