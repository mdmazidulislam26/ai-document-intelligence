"""
Sliding-window rate limiter protecting expensive upload, search, and verification endpoints.
Uses Redis when available and falls back to thread-safe in-memory sliding windows.
"""

import time
import threading
from collections import defaultdict, deque
from typing import Callable, Optional
from fastapi import Request, HTTPException, status
import redis
from core.config import settings


class RateLimiter:
    _mem_lock = threading.Lock()
    _mem_buckets: dict[str, deque] = defaultdict(deque)
    _redis_client: Optional[redis.Redis] = None

    @classmethod
    def _get_redis(cls) -> Optional[redis.Redis]:
        if cls._redis_client is None:
            try:
                client = redis.Redis.from_url(settings.REDIS_URL, socket_connect_timeout=0.5, socket_timeout=0.5)
                client.ping()
                cls._redis_client = client
            except Exception:
                return None
        return cls._redis_client

    @classmethod
    def reset(cls) -> None:
        """Clears rate limit buckets (for tests)."""
        with cls._mem_lock:
            cls._mem_buckets.clear()
        client = cls._get_redis()
        if client is not None:
            try:
                for key in client.scan_iter("ratelimit:*"):
                    client.delete(key)
            except Exception:
                pass

    @classmethod
    def check_limit(cls, identifier: str, bucket: str, max_requests: int, window_seconds: int = 60) -> None:
        if not settings.RATE_LIMIT_ENABLED or max_requests <= 0:
            return

        now = time.time()
        redis_key = f"ratelimit:{bucket}:{identifier}"
        client = cls._get_redis()

        if client is not None:
            try:
                pipe = client.pipeline()
                window_start = now - window_seconds
                pipe.zremrangebyscore(redis_key, 0, window_start)
                pipe.zcard(redis_key)
                pipe.zadd(redis_key, {f"{now}:{time.monotonic_ns()}": now})
                pipe.expire(redis_key, window_seconds + 5)
                results = pipe.execute()
                current_count = int(results[1])
                if current_count >= max_requests:
                    raise HTTPException(
                        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                        detail=f"Rate limit exceeded for {bucket}. Maximum {max_requests} requests per {window_seconds}s.",
                        headers={"Retry-After": str(window_seconds)},
                    )
                return
            except HTTPException:
                raise
            except Exception:
                # Fall back to in-memory if Redis temporarily unavailable
                cls._redis_client = None

        with cls._mem_lock:
            dq = cls._mem_buckets[redis_key]
            cutoff = now - window_seconds
            while dq and dq[0] <= cutoff:
                dq.popleft()
            if len(dq) >= max_requests:
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail=f"Rate limit exceeded for {bucket}. Maximum {max_requests} requests per {window_seconds}s.",
                    headers={"Retry-After": str(window_seconds)},
                )
            dq.append(now)


def rate_limit_dependency(bucket: str, limit_getter: Callable[[], int], window_seconds: int = 60):
    async def _limiter(request: Request) -> None:
        client_host = request.client.host if request.client else "unknown"
        api_key = request.headers.get("X-API-Key") or request.headers.get("Authorization") or ""
        ident = f"{client_host}:{hash(api_key)}"
        RateLimiter.check_limit(ident, bucket, limit_getter(), window_seconds=window_seconds)
    return _limiter


rate_limit_upload = rate_limit_dependency("upload", lambda: settings.RATE_LIMIT_UPLOAD_PER_MIN)
rate_limit_search = rate_limit_dependency("search", lambda: settings.RATE_LIMIT_SEARCH_PER_MIN)
rate_limit_write = rate_limit_dependency("write", lambda: settings.RATE_LIMIT_WRITE_PER_MIN)
