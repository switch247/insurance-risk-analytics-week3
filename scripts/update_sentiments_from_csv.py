"""Update sentiment_label and sentiment_score in DB from processed CSV.

This script reads `outputs/models/reviews_with_sentiment_and_themes.csv` and
for each row updates the `reviews` table matching on `orig_review_id`.
"""
from __future__ import annotations

import os
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

import pandas as pd
from src.config import settings
from src.utils.db_helper import PostgresDB


def load_processed():
    p = Path('outputs') / 'models' / 'reviews_with_sentiment_and_themes.csv'
    if not p.exists():
        p = Path(settings.DATA_PATHS.get('processed_reviews'))
    if not p.exists():
        raise FileNotFoundError('Processed CSV not found')
    return pd.read_csv(p)


def main():
    df = load_processed()
    print('Loaded', len(df), 'rows from processed CSV')

    db = PostgresDB()
    db.init_pool()
    try:
        updated = 0
        with db.get_conn() as conn:
            with conn.cursor() as cur:
                for _, row in df.iterrows():
                    orig = str(row.get('review_id'))
                    label = row.get('sentiment_label')
                    score = row.get('sentiment_score')
                    if pd.isna(label) and pd.isna(score):
                        continue
                    cur.execute(
                        "UPDATE reviews SET sentiment_label = %s, sentiment_score = %s WHERE orig_review_id = %s",
                        (label, float(score) if not pd.isna(score) else None, orig),
                    )
                    if cur.rowcount > 0:
                        updated += cur.rowcount
            conn.commit()
        print('Updated rows:', updated)
    finally:
        db.close_pool()


if __name__ == '__main__':
    main()
