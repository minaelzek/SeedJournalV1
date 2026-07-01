from fastapi import APIRouter

from app.api.v1 import account, auth, entries, health, insights, me, memories, reflection, tree

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(me.router, tags=["identity"])
api_router.include_router(account.router, prefix="/me", tags=["account"])
api_router.include_router(insights.router, prefix="/insights", tags=["insights"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(entries.router, prefix="/entries", tags=["journal"])
api_router.include_router(reflection.router, prefix="/entries", tags=["reflection"])
api_router.include_router(memories.router, prefix="/memories", tags=["memories"])
api_router.include_router(tree.router, prefix="/tree", tags=["growth"])