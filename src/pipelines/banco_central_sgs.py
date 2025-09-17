# src/pipelines/banco_central_sgs.py
from __future__ import annotations
import pandas as pd
from common.config import BRONZE_DIR, SILVER_DIR, DEFAULT_HEADERS
from common.io import safe_get, save_json, save_parquet

BASE = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.{id}/dados"

def fetch_sgs_series(series_id: int, inicio: str, fim: str) -> pd.DataFrame:
    def _br(dt: str) -> str:
        d = pd.to_datetime(dt).date()
        return d.strftime("%d/%m/%Y")
    params = {"formato": "json", "dataInicial": _br(inicio), "dataFinal": _br(fim)}
    url = BASE.format(id=series_id)
    r = safe_get(url, params=params, headers=DEFAULT_HEADERS)
    data = r.json()
    save_json(data, BRONZE_DIR / "banco_central_sgs" / f"serie_{series_id}.json")
    df = pd.DataFrame(data) if data else pd.DataFrame(columns=["data", "valor"])
    df["data"] = pd.to_datetime(df["data"], format="%d/%m/%Y", errors="coerce")
    df["valor"] = pd.to_numeric(df["valor"].str.replace(",", "."), errors="coerce")
    df = df.dropna(subset=["data"]).sort_values("data")
    return df

def run(inicio: str, fim: str):
    print("[BCB SGS] Iniciando ingestão...")
    series = {11: "selic_diaria", 433: "ipca"}
    for sid, name in series.items():
        df = fetch_sgs_series(sid, inicio, fim)
        save_parquet(df, SILVER_DIR / "banco_central_sgs" / f"{name}.parquet")
        print(f"[BCB SGS] {name}: {len(df)} registros")
