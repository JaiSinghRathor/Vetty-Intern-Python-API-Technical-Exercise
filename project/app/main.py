# app/main.py

from __future__ import annotations

from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordRequestForm

from app import auth
from app.auth import Token
from app.config import get_settings
from app.routers import categories, coins, meta

settings = get_settings()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Crypto market updates API (INR & CAD) built on CoinGecko.",
)


@app.post("/auth/token", response_model=Token, tags=["auth"])
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    """
    Issue a JWT access token.
    Use this token with `Authorization: Bearer <token>` for protected endpoints.
    """
    return await auth.login_for_access_token(form_data)


app.include_router(meta.router)
app.include_router(coins.router)
app.include_router(categories.router)
