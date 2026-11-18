"""
Token exchange endpoint allowing clients to obtain short-lived HMAC-signed Bearer tokens
in exchange for a valid configured API key.
"""

from fastapi import APIRouter, HTTPException, Header, status
from pydantic import BaseModel
from core.security import verify_api_key, create_access_token
from core.config import settings

router = APIRouter(prefix="/auth", tags=["Authentication"])


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in_seconds: int
    owner_id: str
    role: str


@router.post("/token", response_model=TokenResponse)
async def issue_bearer_token(x_api_key: str = Header(..., alias="X-API-Key")):
    """Exchanges a valid X-API-Key for a signed Bearer token."""
    principal = verify_api_key(x_api_key.strip())
    if principal is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key.",
        )

    token = create_access_token(owner_id=principal.owner_id, role=principal.role)
    return TokenResponse(
        access_token=token,
        expires_in_seconds=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        owner_id=principal.owner_id,
        role=principal.role,
    )
