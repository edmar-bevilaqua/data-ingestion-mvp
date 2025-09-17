from __future__ import annotations
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data"
BRONZE_DIR = DATA_DIR / "bronze"
SILVER_DIR = DATA_DIR / "silver"
for d in (BRONZE_DIR, SILVER_DIR):
    d.mkdir(parents=True, exist_ok=True)

PORTAL_TRANSPARENCIA_TOKEN = os.getenv("PORTAL_TRANSPARENCIA_TOKEN", "").strip()

DEFAULT_HEADERS = {
    "User-Agent": "mvp-ingestao-dados/0.1 (+https://example.com)"
}
