# Vetty Crypto Market API

Python REST API to fetch cryptocurrency market updates from the CoinGecko API.

- Built with **FastAPI**
- Protected with **JWT auth**
- Returns market data in **INR** and **CAD**
- Auto API docs via **Swagger UI** (`/docs`)
- Dockerized for easy deployment
- Basic tests with `pytest`

---

## Features (v1.0)

### Auth

- `POST /auth/token`
  - Body (form, `application/x-www-form-urlencoded`):
    - `username`
    - `password`
  - Response: `{ "access_token": "...", "token_type": "bearer" }`
  - Use the token with `Authorization: Bearer <token>`.

### Coins

- `GET /api/v1/coins`
  - Lists **all coins** (id, symbol, name) with pagination.
  - Query params:
    - `page_num` (default: `1`)
    - `per_page` (default: `10`)
  - Response:
    ```json
    {
      "page_num": 1,
      "per_page": 10,
      "total": 18000,
      "total_pages": 1800,
      "items": [
        {
          "id": "bitcoin",
          "symbol": "btc",
          "name": "Bitcoin"
        }
      ]
    }
    ```

### Categories

- `GET /api/v1/categories`
  - Lists **coin categories** from CoinGecko (with pagination).
  - Query params:
    - `page_num`, `per_page`
  - Response:
    ```json
    {
      "items": [{ "category_id": "layer-1", "name": "Layer 1" }]
    }
    ```

### Markets (Core Requirement)

- `GET /api/v1/coins/markets`
  - Lists **specific coins** by:
    - `ids` – comma-separated CoinGecko IDs (from `/api/v1/coins`)
    - and/or `category` – category id (from `/api/v1/categories`)
  - Market data is returned against **INR** and **CAD** using CoinGecko:
    - `/coins/markets` (for core coin info, INR)
    - `/simple/price` (for INR + CAD market data)
  - Query params:
    - `ids=bitcoin,ethereum`
    - `category=layer-1`
    - `page_num`, `per_page`
  - Example response item:
    ```json
    {
      "id": "bitcoin",
      "symbol": "btc",
      "name": "Bitcoin",
      "market_cap_rank": 1,
      "inr": {
        "price": 5323456.12,
        "market_cap": 1032456789012.0,
        "volume_24h": 123456789.0,
        "change_24h": 1.23,
        "last_updated_at": 1733390000
      },
      "cad": {
        "price": 89000.12,
        "market_cap": 160000000000.0,
        "volume_24h": 40000000.0,
        "change_24h": 1.1,
        "last_updated_at": 1733390000
      }
    }
    ```

### Meta

- `GET /health`
  - Health check for the app and CoinGecko API (`/ping`).
- `GET /version`
  - Returns app name, version and environment.

---

## Running locally

### 1. Clone & install

```bash
git clone https://github.com/<your-username>/vetty-crypto-api.git
cd vetty-crypto-api

python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

pip install -r requirements.txt
```
