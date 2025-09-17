# run.py
import os, sys

# Garante que "src" entre no PYTHONPATH quando rodar sem Poetry
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(BASE_DIR, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from src.pipelines.run_all import main

if __name__ == "__main__":
    main()
