from fastapi import APIRouter
from app.api.v1.endpoints import draft, champions, predictions, analytics

api_router = APIRouter()

api_router.include_router(
    draft.router, prefix="/draft", tags=["draft"]
)
api_router.include_router(
    champions.router, prefix="/champions", tags=["champions"]
)
api_router.include_router(
    predictions.router, prefix="/predictions", tags=["predictions"]
)
api_router.include_router(
    analytics.router, prefix="/analytics", tags=["analytics"]
)