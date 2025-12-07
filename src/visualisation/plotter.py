"""
Plotting Utility
Task 1: Visualization

This script provides helper functions for plotting data.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

class Plotter:
    """Class for generating plots"""

    def __init__(self):
        """Initialize plotter with default style"""
        sns.set_theme(style="whitegrid")
        plt.rcParams["figure.figsize"] = (10, 6)

    def plot_histogram(self, df, column, title=None, xlabel=None, ylabel="Count", bins=20):
        """Plot histogram of a column"""
        plt.figure()
        sns.histplot(data=df, x=column, bins=bins, kde=True)
        plt.title(title or f"Distribution of {column}")
        plt.xlabel(xlabel or column)
        plt.ylabel(ylabel)
        plt.show()

    def plot_bar(self, df, x, y, title=None, xlabel=None, ylabel=None):
        """Plot bar chart"""
        plt.figure()
        sns.barplot(data=df, x=x, y=y)
        plt.title(title or f"{y} by {x}")
        plt.xlabel(xlabel or x)
        plt.ylabel(ylabel or y)
        plt.xticks(rotation=45)
        plt.show()

    def plot_time_series(self, df, date_col, value_col, title=None):
        """Plot time series"""
        plt.figure()
        sns.lineplot(data=df, x=date_col, y=value_col)
        plt.title(title or f"{value_col} over Time")
        plt.xticks(rotation=45)
        plt.show()
