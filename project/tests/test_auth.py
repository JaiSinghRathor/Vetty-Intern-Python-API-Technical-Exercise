# tests/test_auth.py

from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_login_success():
    resp = client.post(
        "/auth/token",
        data={"username": "vetty", "password": "password"},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert "access_token" in body
    assert body["token_type"] == "bearer"


def test_login_failure():
    resp = client.post(
        "/auth/token",
        data={"username": "wrong", "password": "wrong"},
    )
    assert resp.status_code == 401
