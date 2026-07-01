from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health_v1() -> dict[str, str]:
    return {"status": "ok", "service": "seedjournal-api"}