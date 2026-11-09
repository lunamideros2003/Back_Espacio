# Vercel

## Proyecto

- Nombre: `fron-espacio`
- Project ID: `prj_GmjlESjunz1EvAu5o2Pu8vZCG9Aa`
- Framework: Vite
- Build: `npm run build`
- Output: `dist`

## Variable necesaria

```env
VITE_API_URL=https://TU-API.onrender.com
```

Sin barra final. Se configura en **Settings → Environment Variables** y se
aplica a Production. Después hay que hacer **Redeploy**.

## Orden con Supabase

1. Supabase listo y con tablas.
2. Render con la cadena de Supabase.
3. Vercel con `VITE_API_URL` apuntando a Render.

## Comprobar

- Abrir `https://fron-espacio.vercel.app`.
- La portada debe mostrar el lugar automático.
- `/observar` y `/carta` no deben pedir coordenadas.
- En Network, `/api/place` debe responder 200.

## Errores comunes

| Síntoma | Solución |
| --- | --- |
| “No pudimos conectar con el servidor” | Revisar `VITE_API_URL` |
| CORS bloqueado | Agregar el dominio en `CORS_ORIGINS` |
| 404 en `/api/place` | Redesplegar el backend nuevo |
| Cambio de variable sin efecto | Hacer Redeploy en Vercel |
