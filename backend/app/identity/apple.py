import json
from typing import Any

import httpx
from jose import jwk, jwt
from jose.utils import base64url_decode

from app.core.config import Settings

APPLE_JWKS_URL = "https://appleid.apple.com/auth/keys"
APPLE_ISSUER = "https://appleid.apple.com"


class AppleAuthError(Exception):
    pass


async def fetch_apple_jwks() -> dict[str, Any]:
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(APPLE_JWKS_URL)
        response.raise_for_status()
        return response.json()


def _verify_apple_identity_token(identity_token: str, settings: Settings, jwks: dict[str, Any]) -> dict:
    headers = jwt.get_unverified_header(identity_token)
    kid = headers.get("kid")
    if not kid:
        raise AppleAuthError("Missing key id in Apple token")

    key = next((k for k in jwks.get("keys", []) if k.get("kid") == kid), None)
    if not key:
        raise AppleAuthError("Apple public key not found")

    public_key = jwk.construct(key)
    message, encoded_sig = identity_token.rsplit(".", 1)
    decoded_sig = base64url_decode(encoded_sig.encode())
    if not public_key.verify(message.encode(), decoded_sig):
        raise AppleAuthError("Invalid Apple token signature")

    claims = jwt.get_unverified_claims(identity_token)
    if claims.get("iss") != APPLE_ISSUER:
        raise AppleAuthError("Invalid Apple token issuer")
    aud = claims.get("aud")
    if aud != settings.apple_client_id:
        raise AppleAuthError("Invalid Apple token audience")
    if not claims.get("sub"):
        raise AppleAuthError("Missing subject in Apple token")
    return claims


async def verify_apple_identity_token(identity_token: str, settings: Settings) -> dict:
    jwks = await fetch_apple_jwks()
    return _verify_apple_identity_token(identity_token, settings, jwks)


def dev_claims_from_token(identity_token: str) -> dict:
    """Development only: JSON token {\"sub\":\"...\",\"email\":\"...\"}."""
    try:
        data = json.loads(identity_token)
        if "sub" not in data:
            raise AppleAuthError("Dev token must include sub")
        return {"sub": data["sub"], "email": data.get("email")}
    except json.JSONDecodeError as exc:
        raise AppleAuthError("Invalid dev identity token") from exc