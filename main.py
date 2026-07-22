import uvicorn
import logging

from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware

from app.api.api_routing import api_router
from app.database.dependency import engine
from config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
OPENAPI_URL = "/openapi.json"


app = FastAPI(
    docs_url="/docs",
    redoc_url=None,
)
app.include_router(api_router)

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    SessionMiddleware,
    secret_key=settings.secret_key,
    same_site="none",
    https_only=True,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info", proxy_headers=True, reload=True)
