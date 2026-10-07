# AstroIA — API (FastAPI)

Explorador inteligente del universo. Base de datos **SQLite** (`astroia.db`).

## Cómo arrancar

```bash
cd Back_Espacio
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 4000
```

API: http://localhost:4000  
Docs: http://localhost:4000/docs

Usuario demo: `luna@astroia.dev` / `astroia123`

## APIs gratuitas usadas

- NASA APOD e Images API (`DEMO_KEY` o tu clave en https://api.nasa.gov)
- Open-Meteo (nubes y visibilidad)
- Where The ISS At
- Opcional: Groq (`GROQ_API_KEY`) para el chatbot con Llama

Las posiciones de planetas y estrellas se calculan en el servidor con **PyEphem**.
