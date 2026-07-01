from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import Settings, get_settings
from app.core.deps import get_db
from app.core.security import create_access_token
from app.identity.apple import AppleAuthError, dev_claims_from_token, verify_apple_identity_token
from app.identity.service import get_or_create_user_from_apple

router = APIRouter()


class AppleAuthRequest(BaseModel):
    identity_token: str
    authorization_code: str | None = None


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int


@router.post("/apple", response_model=TokenResponse)
async def auth_apple(
    body: AppleAuthRequest,
    session: AsyncSession = Depends(get_db),
    settings: Settings = Depends(get_settings),
) -> TokenResponse:
    try:
        if settings.app_env == "development" and body.identity_token.strip().startswith("{"):
            claims = dev_claims_from_token(body.identity_token)
        else:
            claims = await verify_apple_identity_token(body.identity_token, settings)
    except AppleAuthError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)) from exc

    user = await get_or_create_user_from_apple(
        session,
        apple_sub=claims["sub"],
        email=claims.get("email"),
    )
    await session.commit()

    token, expires_in = create_access_token(user.id, settings)
    return TokenResponse(access_token=token, expires_in=expires_in)