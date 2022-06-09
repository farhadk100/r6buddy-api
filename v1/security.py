from fastapi import Security, HTTPException
from fastapi.security.api_key import APIKeyHeader

from core.config import settings

api_key_header = APIKeyHeader(name="X-API-KEY")


async def get_api_key(key: str = Security(api_key_header)):
    if key != settings.R6BUDDY_API_KEY:
        raise HTTPException(status_code=401)
