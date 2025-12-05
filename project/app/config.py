# app/config.py

from __future__ import annotations

import os
from functools import lru_cache
from typing import Any, Dict


class Settings:
    """Application configuration loaded from environment variables."""

    APP_NAME: str = "Vetty Crypto Market API"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    COINGECKO_BASE_URL: str
    COINGECKO_API_KEY_HEADER_NAME: str
    COINGECKO_API_KEY: str | None

    def __init__(self) -> None:
        self.ENVIRONMENT = os.getenv("ENVIRONMENT", "dev")

        self.JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "change-this-in-production")
        self.JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
        self.ACCESS_TOKEN_EXPIRE_MINUTES = int(
            os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60")
        )

        # CoinGecko
        # Public docs: https://docs.coingecko.com/ :contentReference[oaicite:0]{index=0}
        self.COINGECKO_BASE_URL = os.getenv(
            "COINGECKO_BASE_URL", "https://api.coingecko.com/api/v3"
        )
        # CoinGecko demo/pro key header names from docs: `x-cg-demo-api-key` / `x-cg-pro-api-key` :contentReference[oaicite:1]{index=1}
        self.COINGECKO_API_KEY_HEADER_NAME = os.getenv(
            "COINGECKO_API_KEY_HEADER_NAME", "x-cg-demo-api-key"
        )
        self.COINGECKO_API_KEY = os.getenv("COINGECKO_API_KEY")

        # Simple in-memory demo credentials (for assignment only)
        self.API_USERNAME = os.getenv("API_USERNAME", "vetty")
        self.API_PASSWORD = os.getenv("API_PASSWORD", "password")

    def as_dict(self) -> Dict[str, Any]:
        return {
            "app_name": self.APP_NAME,
            "app_version": self.APP_VERSION,
            "environment": self.ENVIRONMENT,
        }


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
