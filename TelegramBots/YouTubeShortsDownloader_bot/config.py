from pathlib import Path
import os
import string


BASE_DIR = Path(__file__).resolve().parent

API_TOKEN = os.getenv("API_TOKEN", '')

REPLACEABLE_SYMBOLS = string.punctuation.replace('(', '').replace(')', 
        '').replace('[', '').replace(']', '').replace('&', '').replace('-', 
                '').replace('!', '')
