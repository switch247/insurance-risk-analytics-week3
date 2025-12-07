# Dependencies & Setup

This project depends on a mix of standard data libraries and optional NLP/modeling libraries.

Preferred installation (from project root):

```powershell
pip install -r requirements.txt
```

Notes and optional installs

- NLTK (required for VADER):
  - After installing NLTK, download required corpora:

```powershell
python -c "import nltk; nltk.download('vader_lexicon'); nltk.download('punkt'); nltk.download('stopwords')"
```

- scikit-learn: used for TF-IDF, NMF topic modeling.
- joblib: optional but used to save fitted models.
- transformers: optional, only required if you set `method='transformer'` in the pipeline. Installing `transformers` and `torch`/`tensorflow` may be required depending on the model.

Troubleshooting

- OSError when writing files: ensure `outputs/models` exists and is writable. The notebook and pipeline create parent directories automatically, but if you encounter permission issues, check file system permissions.
- If sentiment transformers fallback unexpectedly to VADER, confirm `transformers` is installed and internet access is available to download model weights.

If you need a minimal set of packages for Task 2 (VADER + topic modeling), ensure at least these are installed:

- pandas
- numpy
- scikit-learn
- nltk
- joblib
- matplotlib
- seaborn

These are typically present in `requirements.txt` for the project; run `pip install -r requirements.txt`.
