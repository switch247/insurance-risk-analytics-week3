("""Evaluation and reporting utilities for sentiment and theme pipelines.

Provides lightweight helpers to check coverage, summarize theme counts
and save small metric reports to disk.
""")
from typing import Dict, Any
import pandas as pd
import json
import os


def evaluate_sentiment_coverage(df: pd.DataFrame, score_col: str = 'sentiment_score') -> float:
	"""Return fraction (0-1) of rows with non-null sentiment scores."""
	if score_col not in df.columns:
		return 0.0
	total = len(df)
	if total == 0:
		return 0.0
	non_null = df[score_col].notna().sum()
	return non_null / total


def summarize_theme_counts(df: pd.DataFrame, bank_col: str = 'bank_name', theme_col: str = 'theme') -> pd.DataFrame:
	"""Summarize counts of themes per bank. Expects `theme` to be a string or list.

	Returns a DataFrame with columns: bank_name, theme, count
	"""
	if bank_col not in df.columns or theme_col not in df.columns:
		return pd.DataFrame(columns=[bank_col, theme_col, 'count'])

	rows = []
	for bank, grp in df.groupby(bank_col):
		for t in grp[theme_col].dropna():
			if isinstance(t, (list, tuple)):
				for theme in t:
					rows.append((bank, theme))
			else:
				rows.append((bank, t))

	if not rows:
		return pd.DataFrame(columns=[bank_col, theme_col, 'count'])

	summary = pd.DataFrame(rows, columns=[bank_col, theme_col])
	summary = summary.groupby([bank_col, theme_col]).size().reset_index(name='count')
	return summary


def save_metrics(metrics: Dict[str, Any], path: str):
	"""Save metrics dict to JSON file at `path` (creates parent dirs)."""
	os.makedirs(os.path.dirname(path), exist_ok=True)
	with open(path, 'w', encoding='utf-8') as f:
		json.dump(metrics, f, indent=2)


def save_sentiment_theme_csv(df: pd.DataFrame, path: str):
	"""Save DataFrame to CSV and ensure parent dirs exist."""
	os.makedirs(os.path.dirname(path), exist_ok=True)
	df.to_csv(path, index=False)

