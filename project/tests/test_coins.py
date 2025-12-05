# tests/test_coins.py

from __future__ import annotations

from typing import Any, Dict, List

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def _get_token() -> str:
    resp = client.post(
        "/auth/token",
        data={"username": "vetty", "password": "password"},
    )
    assert resp.status_code == 200
    return resp.json()["access_token"]


def test_coins_requires_auth():
    resp = client.get("/api/v1/coins")
    assert resp.status_code == 401


def test_health_endpoint():
    resp = client.get("/health")
    assert resp.status_code == 200
    body = resp.json()
    assert "status" in body


def test_version_endpoint():
    resp = client.get("/version")
    assert resp.status_code == 200
    body = resp.json()
    assert body["app_name"] == "Vetty Crypto Market API"
