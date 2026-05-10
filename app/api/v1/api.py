from fastapi import APIRouter

from app.api.v1.routes.items import router as items_router


api_router = APIRouter()


@api_router.get("/health", tags=["Health"])
def health_check() -> dict[str, str]:
    return {
        "status": "healthy",
        "service": "FastAPI Homelab Backend",
    }


api_router.include_router(items_router)