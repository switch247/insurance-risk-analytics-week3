import pandas as pd
import numpy as np
import uuid
from datetime import datetime, timedelta


def _random_headline() -> str:
    # Simple synthetic headline generator
    verbs = ["Rises", "Falls", "Surges", "Drops", "Climbs", "Plummets"]
    adjectives = ["Strong", "Weak", "Unexpected", "Steady", "Volatile"]
    nouns = ["Stock", "Share", "Price", "Value", "Quote"]
    return f"{np.random.choice(adjectives)} {np.random.choice(nouns)} {np.random.choice(verbs)}"


def _random_url() -> str:
    # Generate a dummy URL using a UUID
    return f"https://news.example.com/{uuid.uuid4().hex}"


def _random_publisher() -> str:
    publishers = ["Bloomberg", "Reuters", "CNBC", "Yahoo Finance", "MarketWatch", "WSJ"]
    return np.random.choice(publishers)


def _random_stock() -> str:
    # Simple list of ticker symbols
    tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "NVDA"]
    return np.random.choice(tickers)


def generate_sample_df(name: str = "Sample", n_days: int = 30, freq: str = "D", seed: int | None = None) -> pd.DataFrame:
    """Generate a synthetic DataFrame for testing.

    Parameters
    ----------
    name: str
        Base name for the dataset (currently unused but kept for API compatibility).
    n_days: int
        Number of days to generate data for.
    freq: str
        Frequency string compatible with pandas date_range (e.g., "D", "H").
    seed: int | None
        Random seed for reproducibility.

    Returns
    -------
    pd.DataFrame
        DataFrame with columns: ``headline``, ``url``, ``publisher``, ``date``, ``stock``.
    """
    if seed is not None:
        np.random.seed(seed)

    # Create a date range
    start = pd.Timestamp(datetime.now().date())
    dates = pd.date_range(start=start, periods=n_days, freq=freq)

    data = {
        "headline": [_random_headline() for _ in range(len(dates))],
        "url": [_random_url() for _ in range(len(dates))],
        "publisher": [_random_publisher() for _ in range(len(dates))],
        "date": dates,
        "stock": [_random_stock() for _ in range(len(dates))],
    }
    df = pd.DataFrame(data)
    return df


def generate_sample_reviews(n: int = 100, seed: int | None = None) -> pd.DataFrame:
    """Generate a small synthetic reviews DataFrame for testing the pipelines.

    Columns: review_id, review_text, rating, date, bank_name
    """
    if seed is not None:
        np.random.seed(seed)

    banks = [
        'Commercial Bank of Ethiopia',
        'Bank of Abyssinia',
        'Dashen Bank'
    ]

    sample_texts = [
        'App crashes when sending money',
        'Login failed multiple times',
        'Very fast transfers and easy to use',
        'Slow UI and occasional timeouts',
        'Customer support was helpful',
        'Payment failed but refunded later',
        'Great app, love the design',
        'Bug when uploading ID documents',
        'Fingerprint login not working',
        'Cannot link bank account'
    ]

    rows = []
    for i in range(n):
        review = np.random.choice(sample_texts)
        rating = int(np.random.choice([1,2,3,4,5], p=[0.15,0.15,0.2,0.25,0.25]))
        bank = np.random.choice(banks)
        date = pd.Timestamp(datetime.now()) - pd.to_timedelta(np.random.randint(0, 365), unit='d')
        rows.append({
            'review_id': str(uuid.uuid4()),
            'review_text': review,
            'rating': rating,
            'date': date,
            'bank_name': bank
        })

    return pd.DataFrame(rows)
