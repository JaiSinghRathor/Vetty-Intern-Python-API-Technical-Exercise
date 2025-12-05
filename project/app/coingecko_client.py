# app/coingecko_client.py

from __future__ import annotations

from typing import Any, Dict, List, Optional

import httpx

from app.config import get_settings

settings = get_settings()


class CoinGeckoClient:
    """Thin async client around CoinGecko REST API."""

    def __init__(self) -> None:
        self.base_url = settings.COINGECKO_BASE_URL
        self.api_key = settings.COINGECKO_API_KEY
        self.api_key_header_name = settings.COINGECKO_API_KEY_HEADER_NAME

    def _headers(self) -> Dict[str, str]:
        headers: Dict[str, str] = {}
        if self.api_key:
            headers[self.api_key_header_name] = self.api_key
        return headers

    async def list_coins(self) -> List[Dict[str, Any]]:
        """
        /coins/list – list all supported coins with id, symbol, name. :contentReference[oaicite:2]{index=2}
        """
        url = f"{self.base_url}/coins/list"
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(url, headers=self._headers())
            resp.raise_for_status()
            return resp.json()

    async def list_categories(self) -> List[Dict[str, Any]]:
        """
        /coins/categories/list – list all coin categories. :contentReference[oaicite:3]{index=3}
        """
        url = f"{self.base_url}/coins/categories/list"
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(url, headers=self._headers())
            resp.raise_for_status()
            return resp.json()

    async def coins_markets(
        self,
        ids: Optional[List[str]],
        category: Optional[str],
        page_num: int,
        per_page: int,
    ) -> List[Dict[str, Any]]:
        """
        /coins/markets – list coins with market data vs INR. :contentReference[oaicite:4]{index=4}
        """
        url = f"{self.base_url}/coins/markets"
        params: Dict[str, Any] = {
            "vs_currency": "inr",
            "order": "market_cap_desc",
            "per_page": per_page,
            "page": page_num,
            "sparkline": False,
        }
        if ids:
            params["ids"] = ",".join(ids)
        if category:
            params["category"] = category

        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(url, params=params, headers=self._headers())
            resp.raise_for_status()
            return resp.json()

    async def prices_inr_cad(
        self,
        ids: List[str],
    ) -> Dict[str, Any]:
        """
        /simple/price – prices & market data for given ids vs INR & CAD. :contentReference[oaicite:5]{index=5}
        """
        if not ids:
            return {}

        url = f"{self.base_url}/simple/price"
        params = {
            "ids": ",".join(ids),
            "vs_currencies": "inr,cad",
            "include_market_cap": "true",
            "include_24hr_vol": "true",
            "include_24hr_change": "true",
            "include_last_updated_at": "true",
        }

        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(url, params=params, headers=self._headers())
            resp.raise_for_status()
            return resp.json()

    async def ping(self) -> bool:
        """
        /ping – check if CoinGecko API is alive. :contentReference[oaicite:6]{index=6}
        """
        url = f"{self.base_url}/ping"
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.get(url, headers=self._headers())
            return resp.status_code == 200


def get_coingecko_client() -> CoinGeckoClient:
    return CoinGeckoClient()
