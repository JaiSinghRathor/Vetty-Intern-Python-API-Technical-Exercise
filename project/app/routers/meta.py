# app/routers/meta.py

from __future__ import annotations

from fastapi import APIRouter, Depends

from app.coingecko_client import CoinGeckoClient, get_coingecko_client
from app.config import get_settings

router = APIRouter(tags=["meta"])


@router.get("/health", summary="Health check for app and CoinGecko")
async def health(
    client: CoinGeckoClient = Depends(get_coingecko_client),
):
    coingecko_ok = await client.ping()
    return {
        "status": "ok" if coingecko_ok else "degraded",
        "coingecko": coingecko_ok,
    }


@router.get("/version", summary="Application version info")
async def version():
    settings = get_settings()
    return settings.as_dict()
