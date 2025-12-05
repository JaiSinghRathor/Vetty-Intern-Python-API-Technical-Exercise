# app/routers/coins.py

from __future__ import annotations

from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel

from app.auth import User, get_current_active_user
from app.coingecko_client import CoinGeckoClient, get_coingecko_client

router = APIRouter(prefix="/api/v1/coins", tags=["coins"])


class CoinListItem(BaseModel):
    id: str
    symbol: str
    name: str


class PaginatedResponse(BaseModel):
    page_num: int
    per_page: int
    total: int
    total_pages: int
    items: List[Any]


class CurrencyMarketData(BaseModel):
    price: Optional[float] = None
    market_cap: Optional[float] = None
    volume_24h: Optional[float] = None
    change_24h: Optional[float] = None
    last_updated_at: Optional[int] = None


class CoinMarketItem(BaseModel):
    id: str
    symbol: str
    name: str
    image: Optional[str] = None
    market_cap_rank: Optional[int] = None
    inr: CurrencyMarketData
    cad: CurrencyMarketData


@router.get(
    "",
    response_model=PaginatedResponse,
    summary="List all coins with pagination",
)
async def list_coins(
    page_num: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=250),
    current_user: User = Depends(get_current_active_user),
    client: CoinGeckoClient = Depends(get_coingecko_client),
) -> PaginatedResponse:
    all_coins_raw = await client.list_coins()
    total = len(all_coins_raw)
    start_idx = (page_num - 1) * per_page
    end_idx = start_idx + per_page
    items_slice = all_coins_raw[start_idx:end_idx]
    items = [CoinListItem(**c) for c in items_slice]

    total_pages = (total + per_page - 1) // per_page

    return PaginatedResponse(
        page_num=page_num,
        per_page=per_page,
        total=total,
        total_pages=total_pages,
        items=items,
    )


@router.get(
    "/markets",
    response_model=PaginatedResponse,
    summary="List specific coins (by id and/or category) with market data in INR & CAD",
)
async def list_coin_markets(
    ids: Optional[str] = Query(
        None,
        description="Comma-separated list of coin IDs from /api/v1/coins",
    ),
    category: Optional[str] = Query(
        None,
        description="CoinGecko category id (from /api/v1/categories)",
    ),
    page_num: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=250),
    current_user: User = Depends(get_current_active_user),
    client: CoinGeckoClient = Depends(get_coingecko_client),
) -> PaginatedResponse:
    id_list: Optional[List[str]] = (
        [x.strip() for x in ids.split(",") if x.strip()] if ids else None
    )

    if not id_list and not category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one of 'ids' or 'category' must be provided.",
        )

    markets = await client.coins_markets(
        ids=id_list,
        category=category,
        page_num=page_num,
        per_page=per_page,
    )

    if not markets:
        return PaginatedResponse(
            page_num=page_num,
            per_page=per_page,
            total=0,
            total_pages=0,
            items=[],
        )

    # Collect ids for /simple/price to get INR+CAD-specific data
    ids_for_price = [c["id"] for c in markets]
    price_data = await client.prices_inr_cad(ids_for_price)

    items: List[CoinMarketItem] = []
    for coin in markets:
        cid = coin["id"]
        base = {
            "id": cid,
            "symbol": coin.get("symbol"),
            "name": coin.get("name"),
            "image": coin.get("image"),
            "market_cap_rank": coin.get("market_cap_rank"),
        }

        pd = price_data.get(cid, {})

        inr = CurrencyMarketData(
            price=pd.get("inr"),
            market_cap=pd.get("inr_market_cap"),
            volume_24h=pd.get("inr_24h_vol"),
            change_24h=pd.get("inr_24h_change"),
            last_updated_at=pd.get("last_updated_at"),
        )
        cad = CurrencyMarketData(
            price=pd.get("cad"),
            market_cap=pd.get("cad_market_cap"),
            volume_24h=pd.get("cad_24h_vol"),
            change_24h=pd.get("cad_24h_change"),
            last_updated_at=pd.get("last_updated_at"),
        )

        items.append(CoinMarketItem(inr=inr, cad=cad, **base))

    # For markets we don't know the *global* total from CoinGecko pagination in this simple demo.
    # We'll just use the current page length and total_pages=page_num if items exist.
    total = len(items)
    total_pages = page_num if total > 0 else 0

    return PaginatedResponse(
        page_num=page_num,
        per_page=per_page,
        total=total,
        total_pages=total_pages,
        items=items,
    )
