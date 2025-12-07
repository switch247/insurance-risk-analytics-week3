# Notebooks Guide

This project contains two main notebooks for Week 2:

- `notebooks/01_data_collection_and_analysis.ipynb` — Task 1: scraping and preprocessing. This notebook produces the processed CSV used by Task 2.
- `notebooks/02_sentiment_and_thematic_analysis.ipynb` — Task 2: sentiment scoring, theme extraction, model generation and visualisation.

Order of execution

1. Run Task 1 first. The preprocessing notebook writes a processed CSV to the path defined in `src/customer_analytics/config/settings.py` (commonly `data/processed/reviews_processed.csv`). Task 2 requires that file and will raise a clear error if it is missing.

2. Open and run Task 2. The notebook uses the package `CustomerFeedbackPipeline` helper so model generation is performed via the pipeline helper (`pipeline.save_models()`), and all outputs are written to the project root `outputs/models` directory.

How Task 2 saves outputs

- CSVs and metrics: `outputs/models/reviews_with_sentiment_and_themes.csv`, `outputs/models/themes_by_bank.json`, `outputs/models/sentiment_summary_by_bank_rating.csv`, `outputs/models/task2_metrics.json`, `outputs/models/theme_counts.csv`
- Per-bank fitted models (if `joblib` available): saved to `outputs/models/<bank>_topic_model_*` files.

Visualisation notes

- The notebook includes seaborn/matplotlib plots showing sentiment distribution, average sentiment by bank, and top identified themes. If plots don't render in your environment, ensure the notebook kernel supports inline plotting and that `matplotlib` and `seaborn` are installed.

Running the pipeline from CLI

You can run the same pipeline used by the notebook from the command-line wrapper:

```powershell
python scripts\customer_feedback_pipeline.py --data data/processed/reviews_processed.csv --out outputs/models --method vader --n_themes 3
```

Troubleshooting common errors

- "Processed reviews not found": run Task 1 and confirm the processed file path in `src/customer_analytics/config/settings.py`.
- "Cannot save file into a non-existent directory": the pipeline attempts to create parent directories; if this fails, check permissions for the `outputs` directory in the project root.
- Transformers fallback to VADER: install `transformers` and required backend (Torch or TensorFlow) if you want to use transformer-based sentiment.

If you'd like, I can also add a short `docs/setup.md` with platform-specific steps (Windows PowerShell examples) — tell me if you want that.
