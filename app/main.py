from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import settings
from app.database import Base, engine
from app.routers import auth, chat, objects, observe, quiz
from app.seed import seed_if_empty
from app.services.nasa import get_apod

Base.metadata.create_all(bind=engine)
seed_if_empty()

CORS_ORIGINS = settings.cors_list


@asynccontextmanager
async def lifespan(_app: FastAPI):
    print(f"[AstroIA] Origenes CORS permitidos: {CORS_ORIGINS}")
    yield


app = FastAPI(title="AstroIA API", version="1.0.0", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(HTTPException)
async def http_error(_request, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})


@app.get("/api/health")
def health():
    return {"ok": True, "name": "AstroIA API", "stack": "FastAPI"}


@app.get("/api/debug/cors")
def debug_cors(request: Request):
    """Diagnostico: muestra que origen llego y que la API tiene permitido."""
    origin = request.headers.get("origin", "")
    return {
        "originRecibido": origin,
        "permitido": origin in CORS_ORIGINS,
        "origenesPermitidos": CORS_ORIGINS,
        "corsDesdeVariable": [o.strip() for o in settings.cors_origins.split(",") if o.strip()],
    }


@app.get("/api/apod")
async def apod():
    try:
        return {"apod": await get_apod()}
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


app.include_router(auth.router)
app.include_router(objects.router)
app.include_router(observe.router)
app.include_router(quiz.router)
app.include_router(chat.router)


if __name__ == "__main__":
    import os

    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=int(os.getenv("PORT", settings.port)), reload=True)
