"""Prepare insurance dataset for modeling/EDA.

Loads raw pipe-delimited file, applies cleaning from src.features.insurance_data,
adds derived metrics, and writes processed CSV to the configured processed path.
"""
from __future__ import annotations

from pathlib import Path
import sys

# Ensure src package is importable when run via DVC
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from src.config.settings import settings
from src.features.insurance_data import load_insurance_raw, prep_insurance_dataset


def main():
    raw_path: Path = settings.raw_data_path
    out_path: Path = settings.processed_data_path

    print(f"Loading raw data from {raw_path}")
    df_raw = load_insurance_raw(raw_path)
    print(f"Raw shape: {df_raw.shape}")

    df_clean = prep_insurance_dataset(df_raw)
    print(f"Cleaned shape: {df_clean.shape}")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    df_clean.to_csv(out_path, index=False)
    print(f"Saved processed data to {out_path}")


if __name__ == "__main__":
    main()
