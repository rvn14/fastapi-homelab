from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.api import api_router
from app.db.init_db import init_db


APP_NAME = "FastAPI Homelab Backend"
APP_VERSION = "0.1.0"
API_V1_PREFIX = "/api/v1"


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    init_db()
    yield


def create_application() -> FastAPI:
    app = FastAPI(
        title=APP_NAME,
        description=(
            "A FastAPI backend for testing CRUD operations, PostgreSQL connectivity, "
            "Docker deployment, and remote access through the Proxmox home lab."
        ),
        version=APP_VERSION,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        lifespan=lifespan,
    )

    allowed_origins = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(api_router, prefix=API_V1_PREFIX)

    @app.get("/", tags=["Root"])
    def root() -> dict[str, str]:
        return {
            "message": "FastAPI Homelab Backend is running",
            "version": APP_VERSION,
            "docs": "/docs",
            "api": API_V1_PREFIX,
        }

    return app


app = create_application()