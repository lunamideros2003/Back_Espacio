from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import settings
from app.database import Base, engine
from app.routers import auth, chat, objects, observe, quiz
from app.seed import seed_if_empty
from app.services.nasa import get_apod

Base.metadata.create_all(bind=engine)
seed_if_empty()

app = FastAPI(title="AstroIA API", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_list,
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
