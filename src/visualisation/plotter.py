"""Plotting utility with auto-save and inline display."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Optional

import matplotlib.pyplot as plt
import seaborn as sns

from src.config.settings import settings


class Plotter:
    """Lightweight plotting helpers for notebooks and scripts.

    - Always displays plots inline.
    - Automatically saves PNG files to the configured figures directory using a slugified title.
    - Caller only needs to pass the title; no manual paths.
    """

    def __init__(self, figures_dir: Optional[Path] = None):
        sns.set_theme(style="whitegrid")
        plt.rcParams["figure.figsize"] = (10, 6)
        self.figures_dir = Path(figures_dir) if figures_dir else settings.figures_dir
        self.figures_dir.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def _slugify(title: str) -> str:
        slug = re.sub(r"[^a-zA-Z0-9]+", "_", title.strip()).strip("_").lower()
        return slug or "figure"

    @staticmethod
    def _iqr_bounds(series, k: float = 1.5):
        """Return IQR-based lower/upper bounds for a numeric series."""
        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)
        iqr = q3 - q1
        return q1 - k * iqr, q3 + k * iqr

    def _finalize(self, title: str | None, xlabel: str | None, ylabel: str | None):
        if title:
            plt.title(title)
        if xlabel:
            plt.xlabel(xlabel)
        if ylabel:
            plt.ylabel(ylabel)
        plt.tight_layout()

        if title:
            filename = f"{self._slugify(title)}.png"
            out_path = self.figures_dir / filename
            out_path.parent.mkdir(parents=True, exist_ok=True)
            plt.savefig(out_path, dpi=300)

        plt.show()
        plt.close()

    def plot_histogram(
        self,
        df,
        column,
        title=None,
        xlabel=None,
        ylabel="Count",
        bins=30,
        hue=None,
        kde=True,
        log_scale=False,
    ):
        """Plot and save a histogram for a numeric column with optional hue/KDE."""
        plt.figure()
        sns.histplot(data=df, x=column, bins=bins, kde=kde, hue=hue, multiple="stack")
        if log_scale:
            plt.xscale("log")
        self._finalize(title or f"Distribution of {column}", xlabel or column, ylabel)

    def plot_bar(self, df, x, y, title=None, xlabel=None, ylabel=None, top_n: int | None = None, order=None):
        """Plot and save a bar chart, optionally limiting to top N categories."""
        data = df.copy()
        if top_n and x in data.columns:
            data = data.nlargest(top_n, y)
        plt.figure()
        sns.barplot(data=data, x=x, y=y, order=order)
        plt.xticks(rotation=45)
        self._finalize(title or f"{y} by {x}", xlabel or x, ylabel or y)

    def plot_time_series(self, df, date_col, value_col, title=None, xlabel=None, ylabel=None):
        """Plot and save a time series line chart."""
        plt.figure()
        sns.lineplot(data=df, x=date_col, y=value_col, marker="o")
        plt.xticks(rotation=45)
        self._finalize(title or f"{value_col} over Time", xlabel or date_col, ylabel or value_col)

    def plot_box(self, df, y, x=None, title=None, xlabel=None, ylabel=None, hue=None):
        """Plot and save a boxplot (optionally grouped by x/hue)."""
        plt.figure()
        sns.boxplot(data=df, x=x, y=y, hue=hue)
        plt.xticks(rotation=45)
        self._finalize(title or f"Distribution of {y}", xlabel or (x if x else ""), ylabel or y)

    def plot_scatter(
        self,
        df,
        x,
        y,
        title=None,
        xlabel=None,
        ylabel=None,
        hue=None,
        alpha: float = 0.5,
        fit_line: bool = False,
    ):
        """Plot and save a scatter plot (optionally with a trend line)."""
        plt.figure()
        sns.scatterplot(data=df, x=x, y=y, hue=hue, alpha=alpha)
        if fit_line:
            sns.regplot(data=df, x=x, y=y, scatter=False, color="black")
        plt.xticks(rotation=45)
        self._finalize(title or f"{y} vs {x}", xlabel or x, ylabel or y)

    def plot_outlier_box(self, df, column, k: float = 1.5, title=None, xlabel=None, ylabel=None):
        """Box plot with IQR whisker lines annotated for quick outlier review."""
        clean_series = df[column].dropna()
        lower, upper = self._iqr_bounds(clean_series, k=k)
        plt.figure()
        sns.boxplot(x=clean_series)
        plt.axvline(lower, color="red", linestyle="--", label=f"Lower ({lower:.2f})")
        plt.axvline(upper, color="red", linestyle="--", label=f"Upper ({upper:.2f})")
        plt.legend()
        self._finalize(title or f"Outlier Check: {column}", xlabel or column, ylabel or (ylabel or ""))
