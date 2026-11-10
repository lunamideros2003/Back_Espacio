# Creación automática de tablas

Con `AUTO_CREATE_TABLES=1` el backend crea las tablas al arrancar. Ya no hace
falta abrir el SQL Editor de Supabase.

## Qué ocurre al iniciar

`app/main.py` ejecuta `init_database()` en este orden:

1. Si `AUTO_CREATE_TABLES` está apagado, no hace nada.
2. En PostgreSQL aplica `supabase/schema.sql` sentencia por sentencia.
3. `Base.metadata.create_all` completa cualquier tabla que falte.
4. `seed_if_empty()` siembra el catálogo solo si está vacío.

En SQLite se omite `schema.sql` porque usa `SERIAL` y `now()`, que son propios
de PostgreSQL. Las pruebas locales siguen funcionando igual.

## Por qué no borra datos

`schema.sql` solo contiene:

- `CREATE TABLE IF NOT EXISTS`
- `CREATE INDEX IF NOT EXISTS`

No hay `DROP`, `TRUNCATE`, `DELETE` ni `ALTER`. Si una tabla ya existe, la
sentencia no hace nada y los datos quedan intactos. Las pruebas
`tests/test_db_schema.py` verifican que el archivo no tenga sentencias
destructivas.

## Estructura respetada

El archivo define 6 tablas y 3 índices:

| Tabla | Relaciones |
| --- | --- |
| `users` | Base de usuarios y JWT |
| `celestial_objects` | Catálogo astronómico |
| `quiz_questions` | `object_id` → `celestial_objects` |
| `quiz_attempts` | `user_id` → `users` |
| `observations` | `user_id` → `users`, `object_id` → `celestial_objects` |
| `chat_messages` | `user_id` → `users` |

Las claves foráneas usan `ON DELETE SET NULL` o `ON DELETE CASCADE` tal como
están escritas en `schema.sql`. Los índices son `ix_users_email`,
`ix_celestial_objects_slug` e `ix_celestial_objects_type`.

## Variables

```env
AUTO_CREATE_TABLES=1
SUPABASE_DB_HOST=aws-1-us-west-2.pooler.supabase.com
SUPABASE_DB_PORT=6543
SUPABASE_DB_NAME=postgres
SUPABASE_DB_USER=postgres.<project-ref>
SUPABASE_DB_PASSWORD=<contraseña-de-la-base>
JWT_SECRET=<clave-larga>
```

`DATABASE_URL` también sirve y tiene prioridad sobre `SUPABASE_DB_*`.

## Cómo comprobar

En los logs de Render debe aparecer:

```
[AstroIA] Esquema aplicado: 9 sentencias.
```

Después:

```bash
curl https://TU-API.onrender.com/api/health/db
```

Debe responder `{"ok":true,"database":"up"}`. Luego abre Supabase →
**Table Editor** y confirma las 6 tablas.

## Si ya ejecutaste schema.sql

No pasa nada. Todas las sentencias son idempotentes. Puedes dejar
`AUTO_CREATE_TABLES=1` como red de seguridad o ponerlo en `0` si prefieres
controlar el esquema a mano.

## Cambiar el esquema más adelante

1. Edita `supabase/schema.sql` usando `IF NOT EXISTS`.
2. Para columnas nuevas usa `ALTER TABLE ... ADD COLUMN IF NOT EXISTS`.
3. Reinicia Render. Las sentencias se aplican en el siguiente arranque.
4. Nunca agregues `DROP` ni `TRUNCATE` al archivo.

## Pruebas

```powershell
.\.venv\Scripts\python.exe -m pytest tests/test_db_schema.py tests/test_init_db.py
```

Cubren:

- Las 6 tablas y los 3 índices.
- El orden `schema → create_all → seed`.
- Que SQLite no ejecute `schema.sql`.
- Que el archivo no tenga sentencias destructivas.
- Que cada `CREATE` sea idempotente.
