from __future__ import annotations
import argparse
from pipelines import banco_central_sgs

def main():
    parser = argparse.ArgumentParser(description="Roda ingestão MVP (IBGE, BCB, CGU, INPE)")
    parser.add_argument("--inicio", type=str, default="2003-01-01", help="Data inicial (BCB SGS)")
    parser.add_argument("--fim", type=str, default="2030-12-31", help="Data final (BCB SGS)")
    args = parser.parse_args()

    banco_central_sgs.run(inicio=args.inicio, fim=args.fim)

if __name__ == "__main__":
    main()
