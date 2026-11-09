# Migrar de SQLite a Supabase

## 1. Preparar Supabase

1. Crear el proyecto.
2. Copiar host, puerto, base, usuario y contraseña.
3. Ejecutar `supabase/schema.sql` en el SQL Editor.

## 2. Probar la conexión

Crear `Back_Espacio/.env`:

```env
SUPABASE_DB_HOST=aws-1-us-west-2.pooler.supabase.com
SUPABASE_DB_PORT=6543
SUPABASE_DB_NAME=postgres
SUPABASE_DB_USER=postgres.<ref>
SUPABASE_DB_PASSWORD=<PASSWORD>
AUTO_CREATE_TABLES=0
JWT_SECRET=<clave-larga>
```

Ejecutar:

```powershell
.\.venv\Scripts\python.exe scripts/check_db.py
.\.venv\Scripts\python.exe scripts/count_rows.py
```

## 3. Sembrar el catálogo

```powershell
.\.venv\Scripts\python.exe scripts/init_db.py
.\.venv\Scripts\python.exe scripts/count_rows.py
```

`init_db.py` es idempotente: crea tablas si faltan y siembra solo cuando el
catálogo está vacío.

## 4. Migrar datos existentes

Si ya hay usuarios o bitácoras en SQLite, exportarlos e importarlos con
`pg_dump`/`psql` o con un script puntual. Para el catálogo no hace falta:
`init_db.py` lo reconstruye.

## 5. Cambiar Render

1. Agregar las variables `SUPABASE_DB_*` o `DATABASE_URL`.
2. Poner `AUTO_CREATE_TABLES=0`.
3. Redeploy.
4. Probar `/api/health/db`.

## 6. Verificar

- Registro y login.
- Guardar una observación.
- Completar un quiz.
- Enviar un mensaje al chat.
- Reiniciar el servicio y confirmar que los datos siguen ahí.

## Volver atrás

Quitar `DATABASE_URL` y las variables `SUPABASE_DB_*`; el backend usa SQLite
otra vez. No borres el archivo `astroia.db` hasta confirmar la migración.
