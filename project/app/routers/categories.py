# app/routers/categories.py

from __future__ import annotations

from typing import Any, Dict, List

from fastapi import APIRouter, Depends, Query

from app.auth import User, get_current_active_user
from app.coingecko_client import CoinGeckoClient, get_coingecko_client
from app.routers.coins import PaginatedResponse
from pydantic import BaseModel

router = APIRouter(prefix="/api/v1/categories", tags=["categories"])


class CategoryItem(BaseModel):
    category_id: str
    name: str


@router.get(
    "",
    response_model=PaginatedResponse,
    summary="List coin categories with pagination",
)
async def list_categories(
    page_num: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=250),
    current_user: User = Depends(get_current_active_user),
    client: CoinGeckoClient = Depends(get_coingecko_client),
) -> PaginatedResponse:
    raw = await client.list_categories()
    total = len(raw)
    start_idx = (page_num - 1) * per_page
    end_idx = start_idx + per_page
    sliced = raw[start_idx:end_idx]

    items: List[CategoryItem] = []
    for c in sliced:
        items.append(
            CategoryItem(
                category_id=c.get("category_id") or c.get("id") or "",
                name=c.get("name") or "",
            )
        )

    total_pages = (total + per_page - 1) // per_page

    return PaginatedResponse(
        page_num=page_num,
        per_page=per_page,
        total=total,
        total_pages=total_pages,
        items=items,
    )
