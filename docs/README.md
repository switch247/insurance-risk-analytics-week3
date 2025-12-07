# Customer Fintech Week 2 — Documentation

This `docs/` folder contains short, focused documentation to help run the project pipelines and notebooks for Task 1 (data preprocessing) and Task 2 (sentiment & thematic analysis).

Files added:
- `docs/dependencies.md` — how to install required packages and NLTK data.
- `docs/notebooks.md` — how to run the notebooks in the correct order and where outputs are saved.

Quick start

1. Create and activate the project's virtual environment (use your preferred tool). Example (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Install NLTK resources (see `docs/dependencies.md`) if running sentiment with VADER.

3. Run Task 1 (`notebooks/01_data_collection_and_analysis.ipynb`) to produce the processed reviews file referenced in Task 2.

4. Run Task 2 (`notebooks/02_sentiment_and_thematic_analysis.ipynb`) — the notebook uses the package pipeline helper and writes outputs to `outputs/models` in the project root.

Useful commands

- Run the pipeline from the CLI (thin wrapper):

```powershell
python scripts\customer_feedback_pipeline.py --data data/processed/reviews_processed.csv --out outputs/models --method vader --n_themes 3
```

- Run tests:

```powershell
pytest -q
```

If you run into issues, see `docs/dependencies.md` and `docs/notebooks.md` for troubleshooting steps.
