# Conectar AstroIA con Supabase

Supabase se usa como **Postgres gestionado**. El backend sigue hablando
SQLAlchemy y JWT propio; el frontend nunca recibe credenciales de la base.

## 1. Crear el proyecto

1. Entra a https://supabase.com y crea un proyecto.
2. Guarda la **contraseña de la base de datos**. No es la `secret key`.
3. Espera a que termine el aprovisionamiento.

## 2. Datos de conexión

En **Project Settings → Database**:

| Dato | Ejemplo |
| --- | --- |
| Host | `aws-1-us-west-2.pooler.supabase.com` |
| Puerto | `6543` (pooler) o `5432` (sesión/directo) |
| Base | `postgres` |
| Usuario | `postgres.<project-ref>` |
| Contraseña | La del proyecto |

El puerto `6543` es el *transaction pooler* y es el recomendado para Render.
Si aparece un error raro de conexión, prueba `5432`.

## 3. Crear las tablas

No hace falta ejecutar nada a mano. Con `AUTO_CREATE_TABLES=1` el backend
aplica `supabase/schema.sql` al arrancar: crea las 6 tablas y los 3 índices
solo si faltan, sin borrar datos.

El paso manual sigue disponible si prefieres revisar el SQL antes: abre
**SQL Editor** y ejecuta `supabase/schema.sql`. Es idempotente, así que se
puede correr varias veces sin errores.

Detalle completo en [`AUTO_CREATE.md`](AUTO_CREATE.md).

```env
AUTO_CREATE_TABLES=1
```

## 4. Configurar el backend

Hay dos formas equivalentes. Usa solo una.

### Opción A: cadena completa

```env
DATABASE_URL=postgresql://postgres.<ref>:<PASSWORD>@aws-1-us-west-2.pooler.supabase.com:6543/postgres?sslmode=require
AUTO_CREATE_TABLES=1
JWT_SECRET=una-clave-larga-y-aleatoria
```

### Opción B: variables separadas

```env
SUPABASE_DB_HOST=aws-1-us-west-2.pooler.supabase.com
SUPABASE_DB_PORT=6543
SUPABASE_DB_NAME=postgres
SUPABASE_DB_USER=postgres.<ref>
SUPABASE_DB_PASSWORD=<PASSWORD>
AUTO_CREATE_TABLES=1
JWT_SECRET=una-clave-larga-y-aleatoria
```

`DATABASE_URL` tiene prioridad. Si no se define y existen las variables
`SUPABASE_DB_*`, el backend arma la cadena automáticamente, codifica la
contraseña y agrega `sslmode=require`.

Deja `AUTO_CREATE_TABLES=1`. Si ya aplicaste el esquema a mano puedes usar `0`,
pero `1` no rompe nada porque el SQL es idempotente.

## 5. Probar en local

```powershell
.\.venv\Scripts\python.exe scripts/check_db.py
.\.venv\Scripts\python.exe scripts/init_db.py
.\.venv\Scripts\python.exe scripts/count_rows.py
```

## 6. Render

En **Render → servicio → Environment**:

| Variable | Valor |
| --- | --- |
| `DATABASE_URL` | Cadena de Supabase, o dejar vacío si usas `SUPABASE_DB_*` |
| `SUPABASE_DB_HOST` | `aws-1-us-west-2.pooler.supabase.com` |
| `SUPABASE_DB_PORT` | `6543` |
| `SUPABASE_DB_NAME` | `postgres` |
| `SUPABASE_DB_USER` | `postgres.<ref>` |
| `SUPABASE_DB_PASSWORD` | Contraseña de la base |
| `AUTO_CREATE_TABLES` | `0` |
| `JWT_SECRET` | Clave larga y aleatoria |
| `NASA_API_KEY` | Tu clave o `DEMO_KEY` |

Comprueba:

```bash
curl https://TU-API.onrender.com/api/health/db
```

## 7. Claves que NO se usan

| Variable | Uso real |
| --- | --- |
| `SUPABASE_URL` | Referencia; no la usa el backend actual |
| `SUPABASE_PUBLISHABLE_KEY` | Solo si se migra a Supabase Auth |
| `SUPABASE_SECRET_KEY` | Nunca en el frontend; no es la contraseña de Postgres |
| `SUPABASE_JWKS_URL` | Solo si se valida Auth de Supabase |

No pongas ninguna de estas en variables `VITE_*`.

## 8. Seguridad

- El rol Postgres omite RLS. Si algún día consultas Supabase desde el
  navegador, activa Row Level Security.
- Rota la contraseña si se filtró.
- Los backups están en **Database → Backups**.

## 9. Checklist

- [ ] Proyecto Supabase creado.
- [ ] `supabase/schema.sql` ejecutado.
- [ ] Variables `SUPABASE_DB_*` o `DATABASE_URL` en Render.
- [ ] `/api/health/db` responde 200.
- [ ] Catálogo sembrado con `scripts/init_db.py`.
- [ ] Login y quiz guardan datos.
