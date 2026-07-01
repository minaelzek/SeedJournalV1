from datetime import datetime, timedelta, timezone
from uuid import UUID

from jose import JWTError, jwt
from pydantic import BaseModel

from app.core.config import Settings


class TokenPayload(BaseModel):
    sub: str
    exp: int


def create_access_token(user_id: UUID, settings: Settings) -> tuple[str, int]:
    expires_min = settings.jwt_access_expire_minutes
    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_min)
    payload = {"sub": str(user_id), "exp": expire}
    token = jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)
    return token, expires_min * 60


def decode_access_token(token: str, settings: Settings) -> UUID:
    try:
        data = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
        payload = TokenPayload.model_validate(data)
        return UUID(payload.sub)
    except (JWTError, ValueError) as exc:
        raise ValueError("Invalid token") from exc