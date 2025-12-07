"""
Data Alignment Module

Functions for normalizing dates and merging news with stock price data.
"""

import pandas as pd
import numpy as np
from typing import Tuple


def normalize_dates(df: pd.DataFrame, date_column: str = 'date') -> pd.DataFrame:
    """
    Normalize dates to trading days (remove weekends/holidays).
    
    Args:
        df: DataFrame with date column
        date_column: Name of the date column
        
    Returns:
        DataFrame with normalized dates
    """
    df = df.copy()
    df[date_column] = pd.to_datetime(df[date_column])
    
    # Remove weekends (Saturday=5, Sunday=6)
    df = df[df[date_column].dt.dayofweek < 5].copy()
    
    # Sort by date
    df.sort_values(date_column, inplace=True)
    df.reset_index(drop=True, inplace=True)
    
    return df


def merge_news_stock_data(news_df: pd.DataFrame, stock_df: pd.DataFrame,
                          ticker: str, news_date_col: str = 'date',
                          stock_date_col: str = 'Date') -> pd.DataFrame:
    """
    Merge news and stock data by date and ticker.
    
    Args:
        news_df: News DataFrame with sentiment scores
        stock_df: Stock price DataFrame
        ticker: Stock ticker symbol
        news_date_col: Date column name in news_df
        stock_date_col: Date column name in stock_df
        
    Returns:
        Merged DataFrame with news sentiment and stock prices
    """
    # Normalize dates
    news_df = news_df.copy()
    stock_df = stock_df.copy()
    
    news_df[news_date_col] = pd.to_datetime(news_df[news_date_col]).dt.date
    stock_df[stock_date_col] = pd.to_datetime(stock_df.index if stock_date_col == 'Date' else stock_df[stock_date_col]).date
    
    # Filter news for specific ticker if ticker column exists
    if 'stock' in news_df.columns:
        news_df = news_df[news_df['stock'] == ticker].copy()
    
    # Merge on date
    merged = pd.merge(
        stock_df,
        news_df,
        left_on=stock_date_col,
        right_on=news_date_col,
        how='left'
    )
    
    # Fill missing sentiment with neutral (0)
    sentiment_cols = [
        'avg_sentiment', 'sentiment_std', 
        'pos_mean', 'neg_mean', 'neu_mean',
        'compound', 'pos', 'neg', 'neu'
    ]
    for col in sentiment_cols:
        if col in merged.columns:
            merged[col].fillna(0, inplace=True)
    
    if 'news_count' in merged.columns:
        merged['news_count'].fillna(0, inplace=True)
    
    return merged


def prepare_ml_features(merged_df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
    """
    Prepare features (X) and labels (y) for ML models.
    
    Args:
        merged_df: Merged news-stock DataFrame
        
    Returns:
        Tuple of (features_df, labels_series)
    """
    df = merged_df.copy()
    
    # Feature columns
    feature_cols = [
        'avg_sentiment', 'sentiment_std', 'news_count',
        'pos_mean', 'neg_mean', 'neu_mean'
    ]
    
    # Filter to available columns
    available_features = [col for col in feature_cols if col in df.columns]
    
    X = df[available_features].copy()
    
    # Create target: 1 if price went up next day, 0 otherwise
    if 'daily_return' in df.columns:
        y = (df['daily_return'] > 0).astype(int)
    else:
        # Calculate returns if not present
        df['Close'] = pd.to_numeric(df['Close'], errors='coerce')
        df['daily_return'] = df['Close'].pct_change()
        y = (df['daily_return'].shift(-1) > 0).astype(int)  # Next day's movement
    
    # Remove rows with NaN
    valid_idx = ~(X.isna().any(axis=1) | y.isna())
    X = X[valid_idx]
    y = y[valid_idx]
    
    return X, y


def validate_date_alignment(merged_df: pd.DataFrame) -> dict:
    """
    Return alignment quality metrics.
    
    Args:
        merged_df: Merged DataFrame
        
    Returns:
        Dictionary with alignment statistics
    """
    stats = {
        'total_rows': len(merged_df),
        'rows_with_news': merged_df['news_count'].gt(0).sum() if 'news_count' in merged_df.columns else 0,
        'rows_without_news': merged_df['news_count'].eq(0).sum() if 'news_count' in merged_df.columns else len(merged_df),
        'date_range': f"{merged_df.index.min()} to {merged_df.index.max()}",
        'missing_sentiment_pct': (merged_df['avg_sentiment'].eq(0).sum() / len(merged_df) * 100) if 'avg_sentiment' in merged_df.columns else 100
    }
    
    return stats
