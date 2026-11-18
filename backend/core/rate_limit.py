"""
Distributed sliding-window rate limiter (GHR-07).
Uses deterministic SHA-256 subject hashing (stable across processes)
and an atomic Redis Lua script so multiple API workers enforce consistent limits
without exposing sensitive keys or raw IPs in Redis.
"""

import time
import hashlib
import threading
from collections import defaultdict, deque
from typing import Callable, Optional
from fastapi import Request, HTTPException, status
import redis
from core.config import settings

# Atomic Redis sliding window Lua script: cleans expired entries, checks count,
# and ONLY adds the new request when under max_requests.
_SLIDING_WINDOW_LUA = """
local key = KEYS[1]
local now = tonumber(ARGV[1])
local window_start = tonumber(ARGV[2])
local max_req = tonumber(ARGV[3])
local ttl = tonumber(ARGV[4])
local member = ARGV[5]

redis.call('ZREMRANGEBYSCORE', key, 0, window_start)
local count = redis.call('ZCARD', key)
if count >= max_req then
    return {0, count}
end
redis.call('ZADD', key, now, member)
redis.call('EXPIRE', key, ttl)
return {1, count + 1}
"""


def compute_rate_limit_subject(client_host: str, credential: str = "") -> str:
    """
    Produces a deterministic, process-independent SHA-256 subject identifier.
    Never embeds raw API keys, tokens, or raw IP addresses in Redis keys.
    """
    raw = f"{client_host.strip()}|{credential.strip()}".encode("utf-8")
    return hashlib.sha256(raw).hexdigest()[:32]


class RateLimiter:
    _mem_lock = threading.Lock()
    _mem_buckets: dict[str, deque] = defaultdict(deque)
    _redis_client: Optional[redis.Redis] = None
    _lua_script = None

    @classmethod
    def _get_redis(cls) -> Optional[redis.Redis]:
        if cls._redis_client is None:
            try:
                client = redis.Redis.from_url(settings.REDIS_URL, socket_connect_timeout=0.5, socket_timeout=0.5)
                client.ping()
                cls._redis_client = client
                cls._lua_script = client.register_script(_SLIDING_WINDOW_LUA)
            except Exception:
                return None
        return cls._redis_client

    @classmethod
    def reset(cls) -> None:
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
    def check_limit(cls, subject_id: str, bucket: str, max_requests: int, window_seconds: int = 60) -> None:
        if not settings.RATE_LIMIT_ENABLED or max_requests <= 0:
            return

        now = time.time()
        redis_key = f"ratelimit:{bucket}:{subject_id}"
        client = cls._get_redis()

        if client is not None and cls._lua_script is not None:
            try:
                window_start = now - window_seconds
                member = f"{now}:{time.monotonic_ns()}"
                allowed, _ = cls._lua_script(
                    keys=[redis_key],
                    args=[now, window_start, max_requests, window_seconds + 5, member],
                )
                if int(allowed) == 0:
                    raise HTTPException(
                        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                        detail=f"Rate limit exceeded for {bucket}. Maximum {max_requests} requests per {window_seconds}s.",
                        headers={"Retry-After": str(window_seconds)},
                    )
                return
            except HTTPException:
                raise
            except Exception:
                cls._redis_client = None
                cls._lua_script = None

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
        credential = request.headers.get("X-API-Key") or request.headers.get("Authorization") or ""
        subject_id = compute_rate_limit_subject(client_host, credential)
        RateLimiter.check_limit(subject_id, bucket, limit_getter(), window_seconds=window_seconds)
    return _limiter


rate_limit_upload = rate_limit_dependency("upload", lambda: settings.RATE_LIMIT_UPLOAD_PER_MIN)
rate_limit_search = rate_limit_dependency("search", lambda: settings.RATE_LIMIT_SEARCH_PER_MIN)
rate_limit_write = rate_limit_dependency("write", lambda: settings.RATE_LIMIT_WRITE_PER_MIN)
