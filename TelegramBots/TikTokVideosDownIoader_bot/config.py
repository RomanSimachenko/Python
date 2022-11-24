import requests
from pathlib import Path
import os


BASE_DIR = Path(__file__).parent

API_TOKEN = os.getenv("API_TOKEN", "")

REQUEST_METHODS = {
    'get': requests.get,
    'post': requests.post
}

URL = "https://ssstik.io/abc"

HEADERS = {
    'authority': 'ssstik.io',
    'accept': '*/*',
    'accept-language': 'uk-UA,uk;q=0.9,en-US;q=0.8,en;q=0.7,ru;q=0.6',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'hx-current-url': 'https://ssstik.io/en',
    'hx-request': 'true',
    'hx-target': 'target',
    'hx-trigger': '_gcaptcha_pt',
    'origin': 'https://ssstik.io',
    'referer': 'https://ssstik.io/en',
    'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/       106.0.0.0 Safari/537.36',
}

PARAMS = {
    'url': 'dl',
}

DATA = {
    'locale': 'en',
    'tt': 'RktzNmti',
}
