from __future__ import annotations
import json
from pathlib import Path
from typing import Any, Dict, Optional, Union, List
import pandas as pd
import requests
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

JSONType = Union[Dict[str, Any], List[Dict[str, Any]]]

class HttpError(RuntimeError):
    pass

@retry(
    reraise=True,
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=1, min=1, max=30),
    retry=retry_if_exception_type((HttpError, requests.RequestException)),
)
def safe_get(url: str, *, params: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None, timeout: int = 30) -> requests.Response:
    resp = requests.get(url, params=params, headers=headers, timeout=timeout)
    if resp.status_code >= 400:
        raise HttpError(f"GET {url} -> {resp.status_code} {resp.text[:200]}")
    return resp

def save_raw(payload: Union[str, bytes], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    mode = "wb" if isinstance(payload, (bytes, bytearray)) else "w"
    with open(path, mode) as f:
        f.write(payload)

def save_json(payload: JSONType, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

def save_parquet(df: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    for col in df.select_dtypes(include=["object"]).columns:
        df[col] = df[col].astype("string")
    df.to_parquet(path, index=False)
