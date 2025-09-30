from fastapi import APIRouter
from app.api.v1.endpoints import evaluate, audit, policies, admin

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(evaluate.router, prefix="/evaluate", tags=["evaluate"])
api_router.include_router(audit.router, prefix="/audit", tags=["audit"])
api_router.include_router(policies.router, prefix="/policies", tags=["policies"])
api_router.include_router(admin.router, prefix="/admin", tags=["admin"])
