import re
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import text

from app.config import settings
from app.database import Base, database_target, engine
from app.db_schema import ensure_schema
from app.routers import auth, chat, iss, objects, observe, place, quiz, sky
from app.seed import seed_if_empty
from app.services.nasa import get_apod
from app.validation import validation_message

CORS_ORIGINS = settings.cors_list
CORS_ORIGIN_REGEX = r"https://fron-espacio[a-z0-9-]*\.vercel\.app|http://(localhost|127\.0\.0\.1):[0-9]+"


def init_database() -> None:
    if not settings.auto_create_tables:
        print("[AstroIA] AUTO_CREATE_TABLES=0: se omite la creacion de tablas.")
        return
    print(f"[AstroIA] Base de datos: {database_target()}")
    if settings.supabase_db_host and not settings.database_url.startswith("sqlite"):
        print("[AstroIA] DATABASE_URL tiene prioridad; SUPABASE_DB_* se ignora.")
    try:
        if engine.dialect.name == "postgresql":
            applied = ensure_schema()
            print(f"[AstroIA] Esquema aplicado: {applied} sentencias.")
        Base.metadata.create_all(bind=engine)
        seed_if_empty()
        print("[AstroIA] Base de datos lista.")
    except Exception as exc:
        print(f"[AstroIA] ERROR de base de datos: {type(exc).__name__}: {exc}")
        print("[AstroIA] La API arranca igual. Revisa /api/health/db y las variables.")


init_database()


@asynccontextmanager
async def lifespan(_app: FastAPI):
    print(f"[AstroIA] Origenes CORS permitidos: {CORS_ORIGINS}")
    yield


app = FastAPI(title="AstroIA API", version="1.0.0", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_origin_regex=CORS_ORIGIN_REGEX,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(HTTPException)
async def http_error(_request, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})


@app.exception_handler(RequestValidationError)
async def request_error(_request, exc: RequestValidationError):
    return JSONResponse(status_code=422, content={"error": validation_message(exc.errors())})


@app.get("/api/health")
def health():
    return {"ok": True, "name": "AstroIA API", "stack": "FastAPI"}


@app.get("/api/health/db")
def health_db():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
    except Exception as exc:
        print(f"[AstroIA] health/db: {type(exc).__name__}: {exc}")
        raise HTTPException(
            status_code=503,
            detail="Base de datos no disponible. Revisa DATABASE_URL y SUPABASE_DB_*.",
        ) from exc
    return {"ok": True, "database": "up"}


@app.get("/api/debug/cors")
def debug_cors(request: Request):
    origin = request.headers.get("origin", "")
    regex_ok = bool(re.fullmatch(CORS_ORIGIN_REGEX, origin))
    return {
        "originRecibido": origin,
        "permitido": origin in CORS_ORIGINS or regex_ok,
        "origenesPermitidos": CORS_ORIGINS,
        "regexPermitido": regex_ok,
        "corsDesdeVariable": [o.strip() for o in settings.cors_origins.split(",") if o.strip()],
    }


@app.get("/api/apod")
async def apod():
    try:
        return {"apod": await get_apod()}
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


app.include_router(place.router)
app.include_router(auth.router)
app.include_router(objects.router)
app.include_router(observe.router)
app.include_router(quiz.router)
app.include_router(chat.router)
app.include_router(sky.router)
app.include_router(iss.router)


if __name__ == "__main__":
    import os

    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=int(os.getenv("PORT", settings.port)), reload=True)

