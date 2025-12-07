"""
Configuration file for Bank Reviews Analysis Project
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Google Play Store App IDs
# Keys: CBE, BOA (Bank of Abyssinia), Dashen

APP_IDS = {
    'CBE': os.getenv('CBE_APP_ID', 'com.combanketh.mobilebanking'),
    'BOA': os.getenv('BOA_APP_ID', 'com.boa.boaMobileBanking'),
    'Dashen': os.getenv('DASHEN_APP_ID', 'com.dashen.dashensuperapp') 
}

# Bank Names Mapping (consistent keys with APP_IDS)
BANK_NAMES = {
    'CBE': 'Commercial Bank of Ethiopia',
    'BOA': 'Bank of Abyssinia',
    'Dashen': 'Dashen Bank'
}

# Scraping Configuration
SCRAPING_CONFIG = {
    'reviews_per_bank': int(os.getenv('REVIEWS_PER_BANK', 400)),
    'max_retries': int(os.getenv('MAX_RETRIES', 3)),
    'lang': 'en',
    'country': 'et'  # Ethiopia
}

# File Paths - Use absolute paths from project root
from pathlib import Path
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent  # Go up to project root
DATA_DIR = PROJECT_ROOT / 'data'

DATA_PATHS = {
    'raw': str(DATA_DIR / 'raw'),
    'processed': str(DATA_DIR / 'processed'),
    'raw_reviews': str(DATA_DIR / 'raw' / 'reviews_raw.csv'),
    'processed_reviews': str(DATA_DIR / 'processed' / 'reviews_processed.csv'),
    'sentiment_results': str(DATA_DIR / 'processed' / 'reviews_with_sentiment.csv'),
    'final_results': str(DATA_DIR / 'processed' / 'reviews_final.csv')
}
