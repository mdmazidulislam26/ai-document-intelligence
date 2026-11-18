"""
Authentication and tenant/owner-scoped authorization utilities.
Rejects known placeholder secrets/tokens in production.
"""

import hmac
import json
import time
import base64
import hashlib
from dataclasses import dataclass
from typing import Optional
from fastapi import Header, HTTPException, status
from core.config import (
    settings,
    KNOWN_INSECURE_SECRETS,
    KNOWN_INSECURE_INTERNAL_TOKENS,
    KNOWN_INSECURE_API_KEYS,
)


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
    secret = (settings.AUTH_SECRET_KEY or "").strip()
    if settings.is_production() and (
        not secret or secret in KNOWN_INSECURE_SECRETS or len(secret) < 32
    ):
        raise RuntimeError("AUTH_SECRET_KEY must be securely configured (>= 32 chars, non-placeholder) in production.")
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
    except RuntimeError:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired bearer token.",
            headers={"WWW-Authenticate": "Bearer"},
        )


def verify_api_key(api_key: str) -> Optional[AuthPrincipal]:
    if settings.is_production() and api_key in KNOWN_INSECURE_API_KEYS:
        return None
    configured_keys = settings.get_api_keys()
    for valid_key, meta in configured_keys.items():
        if settings.is_production() and valid_key in KNOWN_INSECURE_API_KEYS:
            continue
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


async def require_admin_or_internal(
    authorization: Optional[str] = Header(default=None),
    x_api_key: Optional[str] = Header(default=None, alias="X-API-Key"),
    x_internal_service_token: Optional[str] = Header(default=None, alias="X-Internal-Service-Token"),
) -> AuthPrincipal:
    if x_internal_service_token is not None:
        configured_internal = (settings.INTERNAL_SERVICE_TOKEN or "").strip()
        if settings.is_production() and (
            configured_internal in KNOWN_INSECURE_INTERNAL_TOKENS or len(configured_internal) < 24
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Internal service token is not securely configured.",
            )
        if configured_internal and hmac.compare_digest(
            x_internal_service_token.strip().encode("utf-8"),
            configured_internal.encode("utf-8"),
        ):
            return AuthPrincipal(owner_id="__internal_service__", role="admin")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid internal service token.",
        )

    principal = await get_current_principal(authorization=authorization, x_api_key=x_api_key)
    if not principal.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Administrator or trusted internal service privileges required.",
        )
    return principal
