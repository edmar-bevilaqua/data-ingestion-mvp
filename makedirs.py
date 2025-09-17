# Recreate the project structure and zip it (retry after kernel reset)

import os, zipfile, shutil, datetime
from pathlib import Path

BASE = Path("/mnt/data/mvp_ingestao_public_apis")
SRC = BASE / "src"
COMMON = SRC / "common"
PIPE = SRC / "pipelines"
DATA = BASE / "data"
BRONZE = DATA / "bronze"
SILVER = DATA / "silver"

# Clean
if BASE.exists():
    shutil.rmtree(BASE)

# Make dirs
for d in [SRC, COMMON, PIPE, BRONZE, SILVER]:
    d.mkdir(parents=True, exist_ok=True)
