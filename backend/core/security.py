"""
Authentication and tenant/owner-scoped authorization utilities.
Supports:
1. Constant-time X-API-Key verification mapped to owner_id and role.
2. HMAC-SHA256 signed Bearer tokens with expiration (Authorization: Bearer <token>).
Fail-closed in production when credentials or signing secrets are misconfigured.
"""

import hmac
import json
import time
import base64
import hashlib
from dataclasses import dataclass
from typing import Optional
from fastapi import Header, HTTPException, status
from core.config import settings


@dataclass(frozen=True)
class AuthPrincipal:
    owner_id: str
    role: str = "user"

    @property
    def is_admin(self) -> bool:
        return self.role == "admin"


def _b64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def _b64url_decode(data: str) -> bytes:
    padding = "=" * ((4 - len(data) % 4) % 4)
    return base64.urlsafe_b64decode(data + padding)


def _get_signing_key() -> bytes:
    secret = settings.AUTH_SECRET_KEY
    if settings.ENVIRONMENT.lower() == "production" and (
        not secret or secret == "dev-insecure-secret-change-in-production"
    ):
        raise RuntimeError("AUTH_SECRET_KEY must be securely configured in production.")
    return secret.encode("utf-8")


def create_access_token(owner_id: str, role: str = "user", expires_minutes: Optional[int] = None) -> str:
    exp_mins = expires_minutes if expires_minutes is not None else settings.ACCESS_TOKEN_EXPIRE_MINUTES
    header = _b64url_encode(json.dumps({"alg": "HS256", "typ": "JWT"}, separators=(",", ":")).encode("utf-8"))
    payload_dict = {
        "sub": owner_id,
        "role": role,
        "iat": int(time.time()),
        "exp": int(time.time()) + exp_mins * 60,
    }
    payload = _b64url_encode(json.dumps(payload_dict, separators=(",", ":")).encode("utf-8"))
    signing_input = f"{header}.{payload}".encode("ascii")
    sig = hmac.new(_get_signing_key(), signing_input, hashlib.sha256).digest()
    return f"{header}.{payload}.{_b64url_encode(sig)}"


def verify_access_token(token: str) -> AuthPrincipal:
    try:
        parts = token.split(".")
        if len(parts) != 3:
            raise ValueError("Invalid token structure")
        header_b64, payload_b64, sig_b64 = parts
        signing_input = f"{header_b64}.{payload_b64}".encode("ascii")
        expected_sig = hmac.new(_get_signing_key(), signing_input, hashlib.sha256).digest()
        provided_sig = _b64url_decode(sig_b64)

        if not hmac.compare_digest(expected_sig, provided_sig):
            raise ValueError("Invalid token signature")

        payload = json.loads(_b64url_decode(payload_b64).decode("utf-8"))
        if int(payload.get("exp", 0)) < int(time.time()):
            raise ValueError("Token expired")

        owner_id = str(payload.get("sub") or "").strip()
        if not owner_id:
            raise ValueError("Missing subject")
        role = str(payload.get("role") or "user")
        return AuthPrincipal(owner_id=owner_id, role=role)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired bearer token.",
            headers={"WWW-Authenticate": "Bearer"},
        )


def verify_api_key(api_key: str) -> Optional[AuthPrincipal]:
    configured_keys = settings.get_api_keys()
    for valid_key, meta in configured_keys.items():
        if hmac.compare_digest(api_key.encode("utf-8"), valid_key.encode("utf-8")):
            owner_id = str(meta.get("owner_id") or "").strip()
            if not owner_id:
                return None
            return AuthPrincipal(owner_id=owner_id, role=str(meta.get("role") or "user"))
    return None


async def get_current_principal(
    authorization: Optional[str] = Header(default=None),
    x_api_key: Optional[str] = Header(default=None, alias="X-API-Key"),
) -> AuthPrincipal:
    """
    FastAPI authentication dependency.
    Requires either a valid Bearer token or valid X-API-Key header.
    """
    if authorization and authorization.lower().startswith("bearer "):
        token = authorization[7:].strip()
        if token:
            return verify_access_token(token)

    if x_api_key:
        principal = verify_api_key(x_api_key.strip())
        if principal is not None:
            return principal
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Authentication credentials required (X-API-Key or Authorization: Bearer).",
        headers={"WWW-Authenticate": "Bearer"},
    )
